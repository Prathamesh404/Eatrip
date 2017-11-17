from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
# We are creating a function to render the home page-render is used to render the url/
#

def home(request):
    return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign-in')
def restaurant_home(request):
    return render(request, 'restaurant/home.html', {})
