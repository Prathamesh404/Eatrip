import json
from django.http import JsonResponse
from oauth2_provider.models import AccessToken
from EatripApp.models import Restro, Meal, Order, OrderDetails
from EatripApp.serializers import RestaurantSerializer, MealSerializer, OrderSerializer
from django.views.decorators.csrf import csrf_exempt


#######
# CUSTOMER
#######
def customer_get_restaurants(request):
    restaurants = RestaurantSerializer(
        Restro.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"restaurants": restaurants})


def customer_get_meals(request, restaurant_id):
    meals = MealSerializer(
        Meal.objects.filter(restaurant_id = restaurant_id).order_by("-id"),
        many = True,
        context = {"request": request}
    ).data
    return JsonResponse({"meals": meals  })

@csrf_exempt
def customer_add_order(request):
    """
    parameters:
        access_token
        restaurant_id
        address
        order_details( json format,) example:
         [{meal: 1, "quantity": 2}, {meal: 1, "quantity": 2}]
    """
    if request.method == "POST":
        #get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt= timezone.now())

        #get profile
        customer = access_token.user.customer

        #Check whether customer has any order that is not Delivered
        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "fail", "error": "Your last order must be complete"})

        #Check the valid address.
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "Address field seems invalid"})

        #orders Details
        order_details = json.loads(request.POST["order_details"])
        order_total = 0
        for meal in order_details:
            order_total += Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]

        if len(order_details) > 0:
            #1. Create Order
            order = Order.objects.create(
                customer = customer,
                restaurant_id = request.POST["restaurant_id"],
                total = order_total,
                status = Order.COOKING,
                address = request.POST["address"]
            )

            #2. Orer Details.
            for meal in order_details:
                OrderDetails.objects.create(
                    order = order,
                    meal_id = meal["meal_id"],
                    quantity = meal ["quantity"],
                    sub_total = Meal.objects.get(id= meal["meal_id"]).price * meal["quanity"]
                )

            return JsonResponse({"status": "success"})

    return JsonResponse({})

def customer_get_lastest_order(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer
    order = OrderSerializer(Order.objects.filter(customer = customer).last()).data

    return JsonResponse({"order": order})

def customer_driver_location(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer

    # Get driver's location related to this customer's current order.
    current_order = Order.objects.filter(customer = customer, status = Order.DELIVERED).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})

###########
# Restaurant
###########

def restaurant_order_notification(request, last_request_time):
    notification = Order.objects.filter(restaurant = request.user.restaurant,
        create_at__gt = last_request_time).count()


    return JsonResponse({"notification": notification})


#######
#drivers
#######

def driver_get_ready_orders(request):
    orders = OrderSerializer(
        Order.objects.filter(status = Order.Ready, driver = None).order_by("-id"),
        many = True

    ).data
    return JsonResponse({})
@csrf_exempt
def driver_pick_orders(request):
    if request.method == "POST":
        #get an acces token
        access_token =  AccessToken.objects.get(token = request.GET.get("access_token"),
            expires__gt = timezone.now())

        #get driver information
        driver = access_token.user.driver

        #To check only one order at a time.
        if Order.objects.filter(driver = driver).exclude(status = Order.ONTHEWAY):
            return JsonResponse({"status": "failed", "error": "You can pick only one order at at a time."})

        try:
            order = Order.objects.get(
                id = request.POST["order_id"],
                status = Order.READY
            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()

            return JsonResponse({"status": "success"})

        except Order.DoesNotExist:
            return JsonResponse({"status": "failure", "error": "This order has been picked already"})

    return JsonResponse({})

def driver_complete_orders(request):
    # Get token
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    order = Order.objects.get(id = request.POST["order_id"], driver = driver)
    order.status = Order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})


def driver_get_latest_orders(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver
    order = OrderSerializer(
        Order.objects.filter(driver = driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"order": order})

def driver_get_revenue(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    from datetime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]

    for day in current_weekdays:
        orders = Order.objects.filter(
            driver = driver,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        revenue[day.strftime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})

# POST - params: access_token, "lat,lng"
@csrf_exempt
def driver_update_location(request):
    if request.method == "POST":
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        driver = access_token.user.driver

        # Set location string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "success"})
