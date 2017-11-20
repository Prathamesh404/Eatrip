from django import forms
from django.contrib.auth.models import User
from EatripApp.models import Restro

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields= {"username", "password", "first_name", "last_name", "email"}

class RestroForm(forms.ModelForm):
    class Meta:
        model = Restro
        fields= {"name", "phone", "address", "logo"}
