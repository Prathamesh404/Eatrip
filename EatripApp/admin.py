from django.contrib import admin

# Register your models here.
from EatripApp.models import Restro, Customer, Driver

admin.site.register(Restro)
admin.site.register(Customer)
admin.site.register(Driver)
