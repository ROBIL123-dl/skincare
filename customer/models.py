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
    cat_offer=models.PositiveIntegerField(null=False,default=0)
    product_offer=models.PositiveIntegerField(null=False,default=0)
    total_quantity =models.PositiveSmallIntegerField(default=1)

class Payment(models.Model):
    STATUS_CHOICES = [
        ('done', 'Done'),
        ('refund', 'Refund'),
        ('no', 'No'),
    ]
    
    PAYMENT_CATEGORY_CHOICES = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('online_payment', 'Online Payment'),
        ('Wallet', 'Wallet')
    ]

    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer_profile, on_delete=models.CASCADE) 
    transaction_id = models.CharField(max_length=255,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='no'
    )
    vendor=models.ForeignKey(Vendor_profile, on_delete=models.CASCADE)
    
    payment_category = models.CharField(
        max_length=20,
        choices=PAYMENT_CATEGORY_CHOICES,
        default='online_payment'
    )
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Payment {self.payment_id} - {self.transaction_id}"
    
    
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
    coupon_id =models.CharField(default='0')
    coupon_price=models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
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
    cat_offer=models.PositiveIntegerField(
        null=False,default=0)
    product_offer=models.PositiveIntegerField(
        null=False,default=0)
    order_status = models.CharField(
        max_length=20,
        verbose_name=_("Order Status"),
        choices=[
            ("Pending", "Pending"),
            ("Confirmed", "Confirmed"),
            ("Shipping", "Shipping"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
            ("Return", "Return"),
            ("Returned", "Returned"),
        ],
        default="Pending",
        help_text=_("The current status of the order.")
    )
    Payment=models.ForeignKey(Payment, on_delete=models.CASCADE,null=True)
    
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
    
class wallet(models.Model):
    customer=models.ForeignKey(Customer_profile, on_delete=models.CASCADE)
    vendor=models.ForeignKey(Vendor_profile, verbose_name=_("vendor"), on_delete=models.CASCADE)
    product=models.ForeignKey(Products, verbose_name=_(""), on_delete=models.CASCADE)
    total_amount= models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Total Amount"),)
    created_at=models.DateTimeField( auto_now_add=True)
    status=models.CharField(default="null")
    
    class Meta:
        ordering = ['-created_at'] 
         
class Return_product(models.Model):
    customer=models.ForeignKey(Customer_profile, on_delete=models.CASCADE)
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    reason=models.CharField()
    created_at=models.DateTimeField(auto_now_add=True)
    
class Wishlist(models.Model):
    customer=models.ForeignKey(Customer_profile, on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    
    

    
