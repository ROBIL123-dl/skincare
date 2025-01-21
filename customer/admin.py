from django.contrib import admin
from customer.models import Order,Payment,Return_product
# Register your models here.

admin.site.register(Payment) # code for User model registered in django default admin
admin.site.register(Order)
admin.site.register(Return_product)
# admin.site.register(Category)
