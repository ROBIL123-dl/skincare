from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re



#  user registration form

class User_registretion(forms.ModelForm):
    full_name=forms.CharField(
        max_length=40,
        label="Full Name",                                  #full name feild
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Full Name is mandatory!'}
                              )
    
    username= forms.CharField(
        max_length=40,                                    #username feild
        label="Username",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Usename is mandatory!'}
                             )
    
    email = forms.EmailField(
        label="Email id",
        required=True,                                           #email feild
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Email id is mandatory!'}
                           )
    password=forms.CharField(
        min_length=8,
        label="Password",                                        #password feild
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Password is mandatory!'}
                             )
    conform_password=forms.CharField(
        min_length=8,
        label="Conform password",                           #conform password feild
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'conform password is mandatory!'}
                          )
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email','password']
        
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[a-zA-Z\s]+$', full_name):
            raise ValidationError("Full Name must contain only letters and spaces.")
        return full_name
     
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            raise ValidationError("Username can only contain letters, numbers, dots, underscores, and hyphens.")
        return username 
    
    def clean(self):
        symbols=['@','*','#']
        count=0
        cleaned_data=super().clean()                          # form validation funtion
        password=cleaned_data['password']
        conform_password = cleaned_data['conform_password']
        print(password)
        if len(password)>=8:
            passw=list(password)
            print(passw)
            for i in passw:
                if i in symbols:
                    count +=1 
        else:
         
          raise forms.ValidationError("Password should have 8 character")
        if count == 0:
           
            raise forms.ValidationError("Please add symbols in password")
        if password != conform_password:
         
            raise forms.ValidationError("please enter correct password")
          
    def save(self,role=0, commit=True):
        full_name = self.cleaned_data['full_name']
        user_name = self.cleaned_data['username']           # funtion for save forms valid data to User model
        email =  self.cleaned_data['email']
        password =  self.cleaned_data['password']
        if role == 1 or role == 0:
          user=User.objects.create_user(full_name=full_name,
                                      username=user_name,
                                      email=email,
                                      password=password,
                                      is_active=False,
                                      is_staff= False,
                                      Role = role
                                      )
        else:
            user=User.objects.create_user(full_name=full_name,
                                      username=user_name,
                                      email=email,
                                      password=password,
                                      is_active=False,
                                      is_staff= False,
                                      Role = role
                                      )
        return user
    
 # ---------------customer registretion form class closed---------> 
 
# vendor licence register form 
class Vendor_license(forms.ModelForm):
    license=forms.ImageField(
                label="License",
                required=True,
                widget=forms.FileInput(attrs={'class': 'form-control'}),
                error_messages={'required': 'upload your license!'}
             )
    addres = forms.CharField(
    label="Address",
    required=True,
    widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 6,  
        'placeholder': 'Enter your address here...'
    }),
    error_messages={'requirepd': 'Enter your address!'}
      ) 
    phone_number = forms.IntegerField(
    label="Phone Number",
    required=True,
    widget=forms.NumberInput(attrs={'class': 'form-control'}),
    error_messages={'required': 'Enter your phone number!'}
)
    
    photo=forms.ImageField(
                label="image",
                widget=forms.FileInput(attrs={'class': 'form-control'}), 
             )
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number)) != 10:
            raise forms.ValidationError("Phone number must be 10 digits long!")
        return phone_number
    
    class Meta:
        model =Vendor_profile 
        fields = ['license','addres','phone_number','photo']
# closed
   
# user login form 
class customerLogin(forms.Form):
    
    email_id=forms.EmailField(
        
                 label="Email Id",
                 required=True,
                 widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your email id'}),
                 error_messages={'required': 'Enter your email !'}
                            )
    
    password=forms.CharField(
                 label="Password",
                 required=True,
                 widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password','placeholder': 'Enter your password'}),
                 error_messages={'required': 'Enter your password !'}
               )
#closed
# add category form
class CategoryForm(forms.ModelForm):
    name=forms.CharField(
        
        max_length=20,
        label=" Name",                                
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': ' Name is mandatory!'}
                       )
    
    desc = forms.CharField(
      label="Description",
      widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 4,  
        'placeholder': 'Enter description here...'
    }),
    )
    offer_price = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
        error_messages={'required': 'Price is required', 'invalid': 'Please enter a valid price'})
    
    class Meta:
        model =Category 
        fields = ['name','desc','offer_price']
        
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name.replace(' ', '').isalnum():
            raise forms.ValidationError("Name can only contain letters, numbers, and spaces.")
        
        if len(name.strip()) < 2:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        
        return name
        
    def clean_offer_price(self):
        offer_price = self.cleaned_data.get('offer_price')
        if offer_price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return offer_price
#closed 



