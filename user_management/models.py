from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.text import slugify
# Create your models here.

# user model class and it manager class 
# ------------------------->
    #   user model manager class
class CustomUserManager(BaseUserManager):
    def create_user(self, email,username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)                         # user manager code
        print(email)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username, password=None, **extra_fields):
        print(password,email)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True) 
        extra_fields.setdefault('is_active', True) 
        return self.create_user(email,username, password, **extra_fields)
  # -----------user model manager class closed---------------->

# user model
class User(AbstractBaseUser):
    vendor = 2
    customer = 1
    default = 0
    ROLE_CHOICES ={                  
        vendor : 'vendor',
        customer : 'customer',
        default : 'default'
    }
    
    full_name=models.CharField(max_length=50,null=False)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=254,unique=True)
   
    join_date=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    Role=models.PositiveIntegerField(choices=ROLE_CHOICES,blank=True,null=True,default=0)
    is_admin=models.BooleanField(default=False)
    otp  = models.PositiveIntegerField(blank=True, null=True)
    
    
    objects = CustomUserManager()      # manager class
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "username",]
    
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
        #------------- user model closed------------>
    # -----------user model class and it manager class closed-------------->
    
# ----------- customer profile model class-------------->   
class Customer_profile(models.Model):
   
     full_name=models.CharField(max_length=50,null=False)
     phone_number=models.BigIntegerField(null=True)
     photo = models.ImageField(upload_to='media/',null=False)
     date_of_join=models.DateTimeField(auto_now_add=True)
     modification_date=models.DateTimeField(auto_now_add=True)
     customer_id=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
     
     def __str__(self):
        return self.full_name
# ----------- customer profile model class closed-------------->   

    
class customer_address(models.Model):
    ROLE_CHOICES = [
        ('YES', 'current address'),
        ('NO', 'not current address'),
    ]
    
    full_name=models.CharField(max_length=50,null=False)
    addres=models.TextField(max_length=300,null=False)
    country=models.CharField(max_length=20,null=False)
    state=models.CharField(max_length=20,null=False)
    pincode = models.CharField(max_length=20,null=False)
    phone_number=models.CharField(max_length=20,null=True)
    current=models.CharField(choices=ROLE_CHOICES,default=False,blank=True)
    user_id=models.ForeignKey("customer_profile", on_delete=models.CASCADE)
    def __str__(self):
        return self.full_name


# ----------- vendor profile model class-------------->       
class Vendor_profile(models.Model):
    seller_name=models.CharField(max_length=20,null=True,blank=True)
    phone_number=models.BigIntegerField(null=True,blank=True)
    photo = models.ImageField(upload_to='media/',null=True,blank=True)
    status= models.BooleanField(default=False),
    addres=models.TextField(max_length=500,null=True,blank=True)
    license=models.ImageField(upload_to='media/',null=False)
    date_of_join=models.DateTimeField(auto_now_add=True)
    modification_date=models.DateTimeField(auto_now_add=True)
    vendor_id=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.seller_name
# ----------- vendor profile model class closed-------------->   


# ----------- category model class-------------->   

class Category(models.Model):
    name=models.CharField(max_length=20,null=False)
    slug = models.SlugField(unique=True, blank=True)
    desc=models.CharField(max_length=100)
    delete = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it doesn't exist
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
# ----------- category model class closed-------------->   
      
    
    