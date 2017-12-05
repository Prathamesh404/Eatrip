from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from EatripApp.forms import UserForm, RestroForm, UserFormForEdit
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
# We are creating a function to render the home page-render is used to render the url/
#

def home(request):
    return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign-in')
def restaurant_home(request):
    return redirect(restaurant_order)

@login_required(login_url='/restaurant/sign-in')
def restaurant_account(request):
    user_form = UserFormForEdit(instance = request.user)
    restaurant_form = RestroForm(instance = request.user.restaurant)


    return render(request, 'restaurant/account.html', {
        "user_form": user_form,
        "restaurant_form": restaurant_form
})

@login_required(login_url='/restaurant/sign-in')
def restaurant_meal(request):
    return render(request, 'restaurant/meal.html', {})

@login_required(login_url='/restaurant/sign-in')
def restaurant_order(request):
    return render(request, 'restaurant/order.html', {})

@login_required(login_url='/restaurant/sign-in')
def restaurant_report(request):
    return render(request, 'restaurant/report.html', {})




def restaurant_sign_up(request):
    user_form = UserForm()
    restro_form = RestroForm()

    '''
    to make out Signup function work, we tweak it.
    '''
    if request.method == "POST":
        user_form = UserForm(request.POST)
        restro_form = RestroForm(request.POST, request.FILES) # request.files is for logos and other files.

        if user_form.is_valid() and restro_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data) #new user object, cleaned .
            new_restro  = restro_form.save(commit=False) # just create for me, dont put in the database yet.
            new_restro.user = new_user
            new_restro.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]

            ))

            return redirect(restaurant_home)


    return render(request, 'restaurant/sign_up.html', {
        "user_form": user_form,
        "restro_form": restro_form

})
