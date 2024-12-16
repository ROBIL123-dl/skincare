from django.db import models
from django.utils.translation import gettext_lazy as _
from vendor.models import * 
from django.utils.timezone import now
from django.db import models
from user_management.models import *

class Cart(models.Model):
    customer_id = models.ForeignKey(Customer_profile, on_delete=models.CASCADE)
    product_id =models.ForeignKey(Products,on_delete=models.CASCADE)
    product_price=models.PositiveIntegerField(null=False,default=1)
    total_quantity =models.PositiveSmallIntegerField(default=1)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer_profile,  
        verbose_name=_("Customer"),
        on_delete=models.CASCADE
    )
   
    vendor = models.ForeignKey(
        Vendor_profile,
        null=True,  
        verbose_name=_("vendor"),
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Products,
        null=True,  
        verbose_name=_("product"),
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=15,default='null')

    delivery_address = models.TextField(
        verbose_name=_("Delivery Address"),
        help_text=_("The address where the order will be delivered.")
    )
    pincode = models.CharField(
        max_length=10,
        verbose_name=_("Pincode"),
        help_text=_("Postal code of the delivery address.")
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total Amount"),
        help_text=_("The total price of the order.")
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        help_text=_("The quantity of the product ordered.")
    )
    order_status = models.CharField(
        max_length=20,
        verbose_name=_("Order Status"),
        choices=[
            ("Pending", "Pending"),
            ("Confirmed", "Confirmed"),
            ("Shipping", "Shipping"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ],
        default="Pending",
        help_text=_("The current status of the order.")
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        help_text=_("The date and time when the order was created.")
    )
    
    is_ordered = models.BooleanField(
        default=True,
        verbose_name=_("Is Ordered"),
        help_text=_("Indicates whether the order is placed.")
    )

    class Meta:
        ordering = ["-created_at"] 
    
    def save(self, *args, **kwargs):
       
        if not self.pk: 
            self.created_at = now().replace(microsecond=0)
        super().save(*args, **kwargs) 

    def __str__(self):
        return f'{self.id}'
    
