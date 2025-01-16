from django import forms
from user_management.models import *
import re
class customer_profile(forms.ModelForm):
    class Meta:
        model =Customer_profile 
        fields = ['full_name','phone_number','photo']  
         
    full_name=forms.CharField(
        max_length=20,
        required=True,
         widget=forms.TextInput(attrs={'class': 'form-control'}),
                error_messages={'required': 'Enter your name!'}
        )
    
    phone_number=forms.IntegerField(
        max_value=9999999999,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control',}),
        error_messages={'required': 'Enter your phone number!'}
        )
    
    photo = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
                error_messages={'required': 'upload your photo!'}
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number)) != 10:
            raise forms.ValidationError("Phone number must be 10 digits long!")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        # Add cross-field validations here if needed
        return cleaned_data
    
    

class address_form(forms.ModelForm):
    class Meta:
        model =customer_address 
        fields = ['full_name','addres','country','pincode','state','phone_number','current'] 
        
    full_name=forms.CharField(
        max_length=20,
        required=True,
         widget=forms.TextInput(attrs={'class': 'form-control'}),
                error_messages={'required': 'Enter your name!'}
        )
    addres = forms.CharField(
    label="Address",
    required=True,
    widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 4,  
        'placeholder': 'Enter your address here...'
    }),
    )
    country=forms.CharField(
        max_length=15,
        required=True,
         widget=forms.TextInput(attrs={'class': 'form-control'}),
                error_messages={'required': 'Enter your pincode!'}
        )
    state=forms.CharField(
        max_length=20,
        required=True,
         widget=forms.TextInput(attrs={'class': 'form-control'}),
                error_messages={'required': 'Enter your state!'}
        )

    pincode=forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control',}),
        error_messages={'required': 'Enter your pincode!'}
        )
    phone_number=forms.IntegerField(
        max_value=9999999999,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control',}),
        error_messages={'required': 'Enter your phone number!'}
        )
    current=forms.CharField(
        widget=forms.RadioSelect(choices=customer_address.ROLE_CHOICES),
        error_messages={'required': 'please specify the value!'}
    )
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[a-zA-Z\s]+$', full_name):
            raise forms.ValidationError("Full Name must contain only letters and spaces.")
        return full_name
    
    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if len(str(pincode)) != 6:
            raise forms.ValidationError("Pincode must be exactly 6 digits!")
        return pincode

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number)) != 10:
            raise forms.ValidationError("Phone number must be 10 digits long!")
        

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country.isalpha():
            raise forms.ValidationError("Country must contain only letters!")
        return country

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if not state.isalpha():
            raise forms.ValidationError("State must contain only letters!")
        return state

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
class password_form(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['password']
     
    password=forms.CharField(
                 label="Password",
                 required=True,
                 widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password','placeholder': 'Enter your password'}),
                 error_messages={'required': 'Enter your password !'}
               )
    conform_password=forms.CharField(
                 label="Password",
                 required=True,
                 widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password','placeholder': 'Enter your password'}),
                 error_messages={'required': 'Enter your password !'}
               )
    
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
        
class email_form(forms.ModelForm):
     class Meta:
        model = User
        fields = ['email']
     
     old_email = forms.EmailField(
        label="Email id",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
                  )
     
     email = forms.EmailField(
        label="Email id",
        required=True,                                           
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'update your email!'}
                           )
        
    
