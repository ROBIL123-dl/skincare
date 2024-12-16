from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from customer.forms import *
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import *
from .models import *
from customer.models import *
from django.utils.text import slugify
from user_management.models import *
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def vendor_profile(request):
    user = get_object_or_404(User,id=request.user.id)
    vendor_object=get_object_or_404(Vendor_profile,vendor_id=user.id)
    initial_data={
        'full_name':vendor_object.seller_name,
        'phone_number':vendor_object.phone_number,
        'photo'  :vendor_object.photo,
        'address'  :vendor_object.addres
    }
    if request.method == 'POST':
         form= Vendor_profile_form(request.POST,request.FILES)
         if form.is_valid():
             full_name=form.cleaned_data['full_name']
             phone_number=form.cleaned_data['phone_number']
             photo=form.cleaned_data['photo']
             address=form.cleaned_data['address']
             vendor_object.seller_name = full_name
             vendor_object.phone_number=phone_number
             vendor_object.photo=photo
             vendor_object.addres=address
             vendor_object.save()
             messages.success(request,'your profile updated') 
         else:
          print(form.errors)
          messages.error(request,'Please enter valid input')   
    else:
        form = Vendor_profile_form(initial=initial_data)
    context={
        'user':user,
        'vendor':vendor_object,
        'form':form
    }
    return render(request,'vendor/profile.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def user_auth(request,user_id):
    user = get_object_or_404(User,id=user_id)
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if email == user.email and check_password(password,user.password):
            return redirect('vendor:change_password',user_id=user.id)
        else:
           messages.error(request,'Your email id and password is not vaild') 
    return render(request,'vendor/vendor_auth.html',{'user':user,})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def change_password(request,user_id):
     user = get_object_or_404(User,id=user_id)
     if request.method == 'POST':
         form = password_form(request.POST)
         if form.is_valid():
           password = form.cleaned_data['password']  
           user.set_password(password)
           user.save()
           messages.success(request,'Change your password,please Relogin')   
           return redirect('index')
         else:
           messages.error(request,'Enter valid password and add symbols')   
     else:
       form = password_form()
     return render(request,'customer/change_password.html',{'form':form,'user':user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def add_subcategory(request):
    vendor= get_object_or_404(Vendor_profile,vendor_id=request.user.id)
    vendor_category = SubCategory.objects.filter(vendor = vendor)
    if request.method == 'POST':
         category = Main_category(request.POST) 
         sub_category = Subcategory(request.POST)  
         if category.is_valid() and sub_category.is_valid():
            name = sub_category.cleaned_data['name']
            Main = category.cleaned_data['main_cat']
            try:
              slug=slugify(Main)
              category = Category.objects.get(slug=slug)
              sub_cat=SubCategory(sub_name = name)
              sub_cat.main_cat= category
              sub_cat.vendor = vendor
              sub_cat.save()
              messages.success(request,'Category created') 
            except:
                messages.error(request,'Category already exist') 
              
         else:
           messages.error(request,'Enter valid input')     
    else:    
         category = Main_category() 
         sub_category = Subcategory()  

    context={
        'category': category,
        'sub_category': sub_category,
        'vendor_category':vendor_category
    }
    return render(request,'vendor/sub_category.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def create_product(request):
    vendor= get_object_or_404(Vendor_profile,vendor_id=request.user.id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
          category=form.cleaned_data['category']
          product_name=form.cleaned_data['product_name']
          product = form.save(commit=False)
          slug=slugify(category)
          Category = get_object_or_404(SubCategory,slug=slug)
          product.subcategory_id = Category
          product.seller_id = vendor
          product.save()
          messages.success(request,'Add product successfully')  
          return redirect('vendor:create_product')
        else:
          messages.error(request,'Follow vaild instructions then enter valid data') 
    else:
     form = ProductForm()
    context={
        'form':form,
    }
    return render(request, 'vendor/create_product.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def product_list(request):
    vendor = get_object_or_404(Vendor_profile,vendor_id=request.user.id)
    product = Products.objects.filter(seller_id = vendor.id)
    context={
        'products' : product
    }
    return render(request,'vendor/product_list.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def product_update(request,product_id):
    product =get_object_or_404(Products,id=product_id)
    initial_data={
        'product_name':product.product_name,
        'product_subname':product.product_subname,
        'description'  :product.description,
        'price'  : product.price,
        'quantity':product.quantity,
        'brand_name':product.brand_name,
        'product_size':product.product_size,
        'image_1':product.image_1,
        'image_2':product.image_2,
        'image_3':product.image_3,
        'category':product.subcategory_id 
    }
    if request.method == 'POST':
         form = ProductForm(request.POST, request.FILES, instance=product)
         if form.is_valid():
           form.save()
           messages.success(request,'Product updated')
           return redirect('vendor:product_list')
         else:
          messages.error(request,'Follow instructions  then enter valid data')   
    else: 
        form = ProductForm(initial=initial_data)      
    return render(request,'vendor/product_update.html',{'form':form,'product':product})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def block_product(request,product_id,status):
    product =get_object_or_404(Products,id=product_id)
    if status == 'block':
      product.active = False
      product.save()
      messages.success(request,'Product blocked')
    else:
      product.active = True
      product.save()
      messages.success(request,'Product Unblocked')
    return redirect('vendor:product_list')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def order_list(request):
    user = get_object_or_404(User,id=request.user.id)
    vendor = get_object_or_404(Vendor_profile,vendor_id = user)
    orders = Order.objects.filter(vendor=vendor)
    context={
        'orders' : orders
    }
    return render(request,'vendor/order_list.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')
def order_details(request,order_id):
    detail = get_object_or_404(Order,id=order_id)
    
    if request.method == 'POST':
       status = request.POST.get('status')
       detail.order_status = status
       detail.save()
    context={
       'detail': detail,
       
    }
    return render(request,'vendor/order_detail.html',context)