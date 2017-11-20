from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from EatripApp.forms import UserForm, RestroForm

# Create your views here.
# We are creating a function to render the home page-render is used to render the url/
#

def home(request):
    return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign-in')
def restaurant_home(request):
    return render(request, 'restaurant/home.html', {})

def restaurant_sign_up(request):
    user_form = UserForm()
    restro_form = RestroForm()

    return render(request, 'restaurant/sign_up.html', {
        "user_form": user_form,
        "restro_form": restro_form

})
