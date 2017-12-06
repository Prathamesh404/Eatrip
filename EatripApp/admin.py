from django.contrib import admin

# Register your models here.
from EatripApp.models import Restro, Customer, Driver, Meal, Order, OrderDetails

admin.site.register(Restro)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderDetails)
