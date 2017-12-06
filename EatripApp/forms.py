from django import forms
from django.contrib.auth.models import User
from EatripApp.models import Restro, Meal

class UserForm(forms.ModelForm):
    '''
    email and password came from the User model,
    '''
    email = forms.CharField(max_length=100, required=True) #
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields= ["username", "first_name", "last_name", "password", "email"]

class RestroForm(forms.ModelForm):
    class Meta:
        model = Restro
        fields= ["name", "address", "phone", "logo"]

class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True) #

    class Meta:
        model = User
        fields= ["username", "first_name", "last_name",  "email"]

class MealForm(forms.ModelForm):
    """docstring for Meal."""
    class Meta:
        model = Meal
        exclude = ("restaurant", )
