from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Customer_profile
from allauth.socialaccount.models import SocialAccount

@receiver(post_save, sender=SocialAccount)
def save_profile(sender, instance, created, **kwargs):
    if created:  # This block executes only when a SocialAccount is created.
        user = instance.user  # Access the linked User instance.
        extra_data = instance.extra_data  # Data from the social provider.
        # Example: Populate user fields
        user.full_name = extra_data.get('name', '')
        user.Role=1
        user.is_active=True
        user.is_staff=False
        user.save()
        name=extra_data.get('name', '')
        Customer_profile.objects.create(customer_id=user,full_name=name)
        
    
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
           
           

    
        