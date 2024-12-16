from django.contrib import admin
from .models import User,Vendor_profile,Customer_profile,Category
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomAdmin(UserAdmin):
    filter_horizontal=()
    list_filter=()                    #custom admin for user model
    fieldsets=()
    list_display=('full_name','email','Role','join_date')
    
    
    

admin.site.register(User,CustomAdmin) # code for User model registered in django default admin
admin.site.register(Customer_profile)
admin.site.register(Vendor_profile)
admin.site.register(Category)