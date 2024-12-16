from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Customer_profile,customer_address


@receiver(post_save, sender=User)
def create_Customer_profile(sender, instance, created, **kwargs):
    print(created)
    if created:
        if instance.Role == 1: 
          profile = Customer_profile.objects.create(customer_id=instance)
          profile.full_name = instance.full_name
          profile.save()
        else:
           print('not created new user')

    
        