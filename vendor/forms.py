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


import re
from django import forms
from .models import Products, SubCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            'product_name',
            'product_subname',
            'description',
            'price',
            'offer_price',
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
        required=False,
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
    offer_price = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter offer price'}),
        error_messages={'required': 'Offer price is required', 'invalid': 'Please enter a valid price'}
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
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter size (optional)'}),
        error_messages={'required': 'Product size is optional'}
    )
    image_1 = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Primary image is required'}
    )
    image_2 = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False
    )
    image_3 = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False
    )
    category = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Category selection is required'}
    )

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')

        # Regex to validate the product name (alphanumeric and spaces allowed)
        if not re.match(r'^[\s\S]+$', product_name):
          raise forms.ValidationError("Product name can only contain letters, numbers, spaces, and special characters.")

        return product_name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_offer_price(self):
        offer_price = self.cleaned_data.get('offer_price')
        price = self.cleaned_data.get('price')

        if offer_price and price and offer_price >= price:
            raise forms.ValidationError("Offer price must be less than the original price.")
        return offer_price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError("Quantity must be greater than to zero.")
        return quantity


    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')

      
        if product_name and len(product_name.strip()) == 0:
            self.add_error('product_name', "Product name cannot be blank or whitespace.")

        return cleaned_data
