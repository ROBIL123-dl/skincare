from django.db import models
from user_management.models import *
from django.utils.text import slugify
from datetime import datetime
# Create your models here.

class SubCategory(models.Model):
    sub_name = models.CharField(max_length=50,null=False,blank=True)  
    slug = models.SlugField(unique=True)  
    vendor =models.ForeignKey(Vendor_profile, on_delete=models.CASCADE)   
    main_cat = models.ForeignKey(Category,null=False, on_delete=models.CASCADE) 
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it doesn't exist
            self.slug = slugify(self.sub_name)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.sub_name

today = datetime.today()
class Products(models.Model):
    product_name = models.CharField(max_length=100)  
    product_subname = models.CharField(max_length=100, blank=True, null=True) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    offer_price=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    quantity = models.PositiveIntegerField(null=False)  
    brand_name = models.CharField(max_length=100,null=False) 
    product_size = models.CharField(max_length=50, blank=True, null=True)  
    image_1 = models.ImageField(upload_to='media/products/',null=True)  
    image_2 = models.ImageField(upload_to='media/products/',null=True)  
    image_3 = models.ImageField(upload_to='media/products/',null=True) 
    active =models.BooleanField(default=True)
    seller_id = models.ForeignKey(Vendor_profile, on_delete=models.CASCADE,null=False) 
    subcategory_id = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=False) 
    admin_status=models.BooleanField(default=True) 
    availability = models.BooleanField(default=True)  
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name



