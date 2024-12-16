from django import forms
from .models import *
from customer.models import *
from user_management.models import *

class Vendor_profile_form(forms.ModelForm):
    
    class Meta:
        model =Vendor_profile 
        fields = ['seller_name','addres','phone_number','photo']
    photo=forms.ImageField(
                label="image",
                widget=forms.FileInput(attrs={'class': 'form-control'}),
                required=False
               
             )
    full_name=forms.CharField(
        max_length=40,
        label="Full Name",                                  
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Full Name is mandatory!'}
    )
    
    address = forms.CharField(
    label="Address",
    widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 6,  
        'placeholder': 'Enter your address here...'
    }),)
    
    phone_number = forms.IntegerField(
    label="Phone Number",
    widget=forms.NumberInput(attrs={'class': 'form-control'}),
    error_messages={'required': 'Enter your phone number!'}
    )
    
class Subcategory(forms.ModelForm):
      class Meta:
        model =  SubCategory
        fields = ['sub_name']
    
      name=forms.CharField(
        
        max_length=20,
        label=" Name",                                
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': ' Name is mandatory!'}
                       )

class Main_category(forms.ModelForm):
     class Meta:
        model =  Category
        fields = ['name']
     main_cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Please mention category'},
        empty_label="Select a category"
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            'product_name',
            'product_subname',
            'description',
            'price',
            'quantity',
            'brand_name',
            'product_size',
            'image_1',
            'image_2',
            'image_3',
        ]

    product_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
        error_messages={'required': 'Product name is required'}
    )
    product_subname = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product subname (optional)'}),
        error_messages={'required': 'Product subname is optional'}
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter detailed description'}),
        error_messages={'required': 'Description is required'}
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
        error_messages={'required': 'Price is required', 'invalid': 'Please enter a valid price'}
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter available quantity'}),
        error_messages={'required': 'Quantity is required', 'invalid': 'Please enter a valid quantity'}
    )
    brand_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand name'}),
        error_messages={'required': 'Brand name is required'}
    )
    product_size = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter size (optional)'}),
        error_messages={'required': 'Product size is optional'}
    )
    image_1 = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Primary image is required'}
    )
    image_2 = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Secondary image is required'}
    )
    image_3 = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Additional image is required'}
    )
    category = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Category selection is required'}
    )
    


      