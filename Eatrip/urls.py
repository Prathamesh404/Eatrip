"""Eatrip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from EatripApp import views
from django.contrib.auth import views as auth_views #setting alias with use of views.

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^restaurant/sign-in/$', auth_views.login,  #using auth_views django will take are of authentication algorithms
        {'template_name' : 'restaurant/sign_in.html'},
         name = 'restaurant-sign-in'),
    url(r'^restaurant/sign-out', auth_views.logout,
        {'next_page' : '/'},
        name = 'restaurant-sign-out'),
    url(r'^restaurant/$', views.restaurant_home, name=  'restaurant-home'),
    url(r'^restaurant/sign-up',views.restaurant_sign_up,
        name = 'restaurant-sign-up'),
]
