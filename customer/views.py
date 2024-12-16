from django.shortcuts import render,redirect
from django.db.models import Count
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required,user_passes_test
from user_management.utils import email
from django.shortcuts import get_object_or_404,get_list_or_404
from django.contrib.auth.hashers import check_password
from vendor.models import *
from django.db.models import F, Sum
from django.db.models import Q
from .forms import *
from .models import *
from user_management.models import *

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def customerProfile(request):
    user = get_object_or_404(User,id=request.user.id)
    customer=get_object_or_404(Customer_profile,customer_id=user.id)
    initial_data = {
        'full_name':customer.full_name,
        'phone_number':customer.phone_number,
        'photo':customer.photo,
    }
    if request.method == 'POST':
        update_form = customer_profile(request.POST,request.FILES )
        if update_form.is_valid():
            full_name=update_form.cleaned_data['full_name']
            phone_number=update_form.cleaned_data['phone_number']
            photo=update_form.cleaned_data['photo']
           
            customer.full_name=full_name
            customer.phone_number=phone_number
            customer.photo=photo
            customer.save()
            messages.success(request,'User profile updated successfully')
        else:
            messages.error(request,'Please enter valid input for updation')
    else:
        update_form = customer_profile(initial=initial_data)
    return render(request,'customer/profile.html',{'update_form':update_form,'customer':customer})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def address(request,customer_id):
    customer = get_object_or_404(Customer_profile,id=customer_id)
    customerAddress =customer_address.objects.filter(user_id = customer.id).all()
    address_count = customerAddress.aggregate(count=Count('id'))
    try:
        current=customerAddress.get(current='YES')
        customer_current_address=get_object_or_404(customer_address,id=current.id)
    except customer_address.DoesNotExist:
        current = None
    if address_count['count'] < 3:
        count = True
    else:
        count = False
    initial_data={
       'full_name':customer.full_name 
    }
    if request.method == 'POST':
        form = address_form(request.POST)
        if form.is_valid():
            address_status = form.cleaned_data['current']
            if address_status == 'YES':
              if current:
                customer_current_address.current = 'NO'
                customer_current_address.save()
    
            address = form.save(commit=False)
            address.user_id = customer
            address.save()
            messages.success(request,'Add new address')
        else:
          messages.error(request,'Please enter valid input')  
    else:
        form = address_form(initial=initial_data)
    context={
            'form':form,
            'customer':customer,
            'address':customerAddress,
            'count':count,
            'back_url': '/customer:checkout/'
        }
    return render(request,'customer/address.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def delete_address(request,customer_id,address_id):
    address = get_object_or_404(customer_address,id=address_id)
    address.delete()
    messages.success(request,'Delete your address')
    return redirect('customer:address',customer_id)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def update_address(request,address_id):
    customer = get_object_or_404(Customer_profile,customer_id=request.user.id)
    customerAddress =customer_address.objects.filter(user_id = customer.id).all()
    address_objects=get_object_or_404(customer_address,id=address_id)
    try:
      current_address=customerAddress.get(current='YES')
    except customer_address.DoesNotExist:
        current_address =None
    initial_data = {
        'full_name':address_objects.full_name,
        'addres':address_objects.addres,
        'country':address_objects.country,
        'state':address_objects.state,
        'pincode':address_objects.pincode,
        'phone_number':address_objects.phone_number,
        'current':address_objects.current,
    }
    if request.method == 'POST':
        form = address_form(request.POST)
        if form.is_valid():
          full_name = form.cleaned_data['full_name']
          address =form.cleaned_data['addres'] 
          country =form.cleaned_data['country'] 
          state =form.cleaned_data['state'] 
          pincode =form.cleaned_data['pincode'] 
          phone_number =form.cleaned_data['phone_number'] 
          current =form.cleaned_data['current'] 
          if current == 'YES':
              if current_address:
                  current_address.current = 'NO'
                  current_address.save()
          address_objects.full_name=full_name
          address_objects.addres = address
          address_objects.country=country
          address_objects.state=state
          address_objects.pincode=pincode
          address_objects.phone_number=phone_number
          address_objects.current=current
          address_objects.save()
          messages.success(request,'Updated your address ')   
          return redirect('customer:address',customer.id)
        else:
          messages.error(request,'Enter correct value')   
    else:
      form = address_form(initial=initial_data)
    context={
        'address':address_objects,
        'form':form
    }
    return render(request,'customer/update_address.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def user_auth(request,user_id):
    user = get_object_or_404(User,id=user_id)
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,user.email)
        print(password,user.password)
        if email == user.email and check_password(password,user.password):
            return redirect('customer:change_password',user_id=user.id)
        else:
           messages.error(request,'Your email id and password is not vaild') 
    return render(request,'customer/user_auth.html',{'user':user,})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def change_password(request,user_id):
     user = get_object_or_404(User,id=user_id)
     if request.method == 'POST':
         form = password_form(request.POST)
         print(form.errors)
         if form.is_valid():
           print('success')
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
@login_required(login_url='c_login')
def shop(request):
    products = Products.objects.filter(active = True)
    Brand = Products.objects.all().values_list('brand_name',flat=True).distinct()
    Subcategory = SubCategory.objects.all().values_list('sub_name',flat=True).distinct()
    categorY= Category.objects.all().values_list('name',flat=True).distinct()
    print(f'category:{categorY}')
    if request.method == 'POST':
      try:
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        price=request.POST.get('price')
        if brand is not None:
          products = Products.objects.filter(
          Q(price__range=(int(price), int(price) + 200)) 
          & Q(brand_name__icontains=brand)
          &Q(active = True))  
           
        elif category is not None:
         products = Products.objects.filter(
          Q(price__range=(int(price), int(price) + 200))
          & Q(subcategory_id__main_cat__name__icontains=category)
          & Q(active = True))
         
        elif subcategory is not None:
         products = Products.objects.filter(
          Q(price__range=(int(price), int(price) + 200)) 
          & Q(subcategory_id__sub_name__icontains=category)
          &Q(active = True))
         
        else:
            products = Products.objects.filter(
            Q(price__range=(int(price), int(price) + 200))
            &Q(active = True))
      except ValueError: 
          messages.error(request,'Filtered product is not avalilable')
          products = Products.objects.none()    
    context={
        'products':products,
        'Brand':Brand,
        'Subcategory':Subcategory,
        'categorY': categorY
    }
    return render(request,'customer/shop.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def single_product(request,product_id):
    product = get_object_or_404(Products,id = product_id)
    category = Products.objects.filter(subcategory_id = product.subcategory_id)
    
    context={
      'product' : product ,
      'category' : category
    }
    return render(request,'customer/single_product.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def add_to_cart(request,product_id):
    product = get_object_or_404(Products,id=product_id)
    user=get_object_or_404(User,id=request.user.id)
    customer=get_object_or_404(Customer_profile,customer_id=user.id)
    if request.method == "POST":
        quantity = request.POST.get('value')
        if int(quantity )<6:
          cart = Cart(customer_id=customer,product_price=product.price,product_id=product,total_quantity=quantity)
          cart.save()
          messages.success(request,'product add to cart') 
        else:
          messages.error(request,'You cannot buy more than 5 same product') 
        return redirect('customer:single_product',product_id)
    else:
      return redirect('customer:single_product',product_id)  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def view_cart(request,product):
    user=get_object_or_404(User,id=request.user.id)
    customer= get_object_or_404(Customer_profile,customer_id=user)
    try:
       cart_products = Cart.objects.filter(customer_id=customer).annotate(
       total_price=Sum(F('total_quantity') * F('product_price')))
       
       if not cart_products.exists():  
        messages.error(request, 'No products added to the cart.')
    except Cart.ObjectDoesNotExist:
        messages.error(request,'No product added to cart') 

    if product > 0 :
        cart=get_object_or_404(Cart,id = product)
        cart.delete()
        messages.success(request,'delete product from cart') 
    all_total_price = cart_products.aggregate(all_total=Sum('total_price'))
    context={
        'cart_products':cart_products,
        'all_total_price':all_total_price,
        'customer':customer
    }
    return render(request,'customer/cart.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def update_quantity_in_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = request.POST.get('quantity')
        update_product = get_object_or_404(Cart,id=product_id)
        if int(new_quantity) < 6:
           update_product.total_quantity = int(new_quantity)
           update_product.save()
           messages.success(request,'product quantity updated')
        else:
           messages.error(request,'You cannot buy more than 5 same product')  
        return redirect('customer:view_cart',0)
    else:
        return redirect('customer:view_cart',0)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def all_products_checkout(request):
    cart_id=0
    user = get_object_or_404(User,id=request.user.id)
    customer = get_object_or_404(Customer_profile,customer_id=user.id)
    try:
       customer_current_address = get_object_or_404(customer_address,user_id=customer.id,current='YES')
       address = customer_address.objects.filter(user_id=customer.id)
    except customer_address.DoesNotExist:
        messages.error(request,'You have no address,add an current address')
        return redirect('customer:address',customer.id)  
    cart_products=Cart.objects.filter(customer_id=customer.id,product_id__quantity__gt = 0).annotate(
        total_price=F('total_quantity') * F('product_price'))
    total_price = cart_products.aggregate(total=Sum('total_price'))
    total_price=total_price['total'] + 50
    status='all_products_checkout'
    context={
        'cart_products' : cart_products,
        'customer_current_address' : customer_current_address,
        'total_price':total_price,
        'address':address,
        'status':status,
        'cart_id':cart_id,
    }
    return render(request,'customer/checkout.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def single_product_checkout(request,cart_id):
     user = get_object_or_404(User,id=request.user.id)
     customer = get_object_or_404(Customer_profile,customer_id=user.id)
     try:
       customer_current_address = get_object_or_404(customer_address,user_id=customer.id,current='YES')
       address = customer_address.objects.filter(user_id=customer.id)
     except customer_address.DoesNotExist:
        messages.error(request,'You have no address,add an current address')
        return redirect('customer:address',customer.id)  
     cart_products=Cart.objects.filter(id=cart_id).annotate(
        total_price=F('total_quantity') * F('product_price'))
     total_price = cart_products.aggregate(total=Sum('total_price'))
     total_price=total_price['total'] + 50
     status='single_product_checkout'
     for cart_item in cart_products:
       if cart_item.product_id.quantity == 0:
         messages.error(request,'You cannot buy product') 
         return redirect('customer:view_cart',0)
     context={
        'cart_products' : cart_products,
        'customer_current_address' : customer_current_address,
        'total_price':total_price,
        'address':address,
        'status':status,
        'cart_id':cart_id,
     }
     return render(request,'customer/checkout.html',context)
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def checkout_address(request,address_id,status,cart_id):
    address = get_object_or_404(customer_address,id=address_id)
    all_address_of_customer=customer_address.objects.filter(user_id=address.user_id)
    try:
     current_address_from_customer=all_address_of_customer.get(current='YES')
    except customer_address.DoesNotExist:
        current_address_from_customer=None
    current_address_from_customer.current='NO'
    current_address_from_customer.save()
    address.current='YES'
    address.save()
    if status == 'all_products_checkout':
       return redirect('customer:all_products_checkout')
    else:
       return redirect('customer:single_product_checkout',cart_id)
   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')  
def place_order(request,cart_id,status):
      if request.method == 'POST':
        user = get_object_or_404(User,id=request.user.id)
        customer = get_object_or_404(Customer_profile,customer_id=user.id)
        address = get_object_or_404(customer_address,user_id = customer.id,current='YES')
        paymethod = request.POST.get('paymentMethod')
        if int(paymethod) == 3:
            if status == 'single_product_checkout':
                  carts = get_object_or_404(Cart,id = cart_id)
                  order=Order(customer=customer,vendor=carts.product_id.seller_id,
                              product=carts.product_id,delivery_address=address.addres,
                              pincode=address.pincode,phone_number=address.phone_number,
                              total_amount=carts.total_quantity*carts.product_price,
                              quantity=carts.total_quantity
                              )
                  order.save()
                  product = get_object_or_404(Products,id=carts.product_id.id)
                  product.quantity = (product.quantity) - (carts.total_quantity)
                  product.save()
                  carts.delete()
                  print(f'order{order}')
            elif status == 'all_products_checkout':
                 carts = Cart.objects.filter(customer_id=customer.id)
                 for cart in carts:
                   if cart.product_id.quantity > 0:
                     order=Order(customer=customer,vendor=cart.product_id.seller_id,
                              product=cart.product_id,delivery_address=address.addres,
                              pincode=address.pincode,phone_number=address.phone_number,
                              total_amount=cart.total_quantity*cart.product_price,
                              quantity=cart.total_quantity
                              )
                     order.save()
                     product = get_object_or_404(Products,id=cart.product_id.id)
                     product.quantity = (product.quantity) - (cart.total_quantity)
                     product.save()
                     cart.delete()
            current_time =  timezone.now().replace(microsecond=0)
            order_products=Order.objects.filter(created_at = current_time)
            total_amount =order_products.aggregate(total=Sum('total_amount'))
            
        context={
        'order_products' : order_products,
        'total_amount': total_amount
        }
       
      return render(request,'customer/place_order.html',context)
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login') 
def order_history(request):
    order_dates = []
    user = get_object_or_404(User,id=request.user.id)
    customer = get_object_or_404(Customer_profile,customer_id=user.id)
    orders= Order.objects.filter(customer=customer)
    for order in orders:
        if order.created_at:
            delivery_date = order.created_at + timedelta(days=5)
            expect_date = order.created_at + timedelta(days=7)
            order_dates.append({
                'order_id' : order.id,
                'delivery_date': delivery_date,
                'expect_date': expect_date
            })
    context={
        'orders':orders,
        'order_dates': order_dates
    }
    return render(request,'customer/order_history.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def order_cancel(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    product = get_object_or_404(Products,id=order.product.id)
    order.order_status = 'Cancelled'
    order.save()
    product.quantity = product.quantity + order.quantity
    product.save()
    messages.success(request,'Order is cancelled')
    return redirect('customer:order_history')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def search_product(request):
  try:
    if request.method == 'POST':
        search = request.POST.get('search')
        products = Products.objects.filter(product_name__icontains=search)
    else:
        product=[]
  except Exception:
       products=[]
       messages.error(request,'product is not available')
     
  return render(request,'customer/shop.html',{'products':products})
    
    
