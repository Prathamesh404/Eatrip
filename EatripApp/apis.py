from django.http import JsonResponse

from EatripApp.models import Restro
from EatripApp.serializers import RestaurantSerializer

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
    return JsonResponse({})


def customer_add_order(request):
    return JsonResponse({})

def customer_get_lastest_order(request):
    return JsonResponse({})
