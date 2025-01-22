from django.shortcuts import render,redirect
from django.db.models import Count
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.utils.dateparse import parse_datetime
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
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
import json
from user_management.models import *
import razorpay
from django.conf import settings
from django.http import JsonResponse
import pytz
from razorpay.errors import SignatureVerificationError
from django.template.loader import render_to_string
from lushaura.settings import PDFKIT_CONFIG
import pdfkit
from io import BytesIO

# Create your views here.

razorpay_client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

#customer profile
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
#customer address view
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

#address delete
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def delete_address(request,customer_id,address_id):
    address = get_object_or_404(customer_address,id=address_id)
    address.delete()
    messages.success(request,'Delete your address')
    return redirect('customer:address',customer_id)
#closed
#address updated
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
#closed
# customer authentication funtion for rest password
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def user_auth(request,user_id):
    user = get_object_or_404(User,id=user_id)
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if email == user.email and check_password(password,user.password):
            return redirect('customer:change_password',user_id=user.id)
        else:
           messages.error(request,'Your email id and password is not vaild') 
    return render(request,'customer/user_auth.html',{'user':user,})

#reset password
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
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
 
 # customer shop view 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def shop(request,wishlist):
    user = get_object_or_404(User, id=request.user.id)
    customer = get_object_or_404(Customer_profile, customer_id=user)
    products = Products.objects.filter(active = True,admin_status=True)
    Brand = Products.objects.all().values_list('brand_name',flat=True).distinct()
    Subcategory = SubCategory.objects.all().values_list('sub_name',flat=True).distinct()
    categorY= Category.objects.all().values_list('name',flat=True).distinct()
    if wishlist!=0:
            try:
              product = get_object_or_404(Products, id=wishlist)
              wishlist_item = Wishlist.objects.get(product=product,customer=customer)
              if wishlist_item:
                  messages.success(request, "Product already in the wishlist")
                  return redirect('customer:shop', 0)
            except Wishlist.DoesNotExist:
             try:
                user = get_object_or_404(User, id=request.user.id)
                customer = get_object_or_404(Customer_profile, customer_id=user)
                new_wishlist = Wishlist(customer=customer, product=product)
                new_wishlist.save()
                messages.success(request, "Product added to wishlist")
             except Exception as e:
                 messages.error(request, f"An error occurred: {str(e)}")
                 return redirect('customer:shop', 0)
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
          &Q(active = True)
         & Q(admin_status = True)
          )  
           
        elif category is not None:
         products = Products.objects.filter(
          Q(price__range=(int(price), int(price) + 200))                 # shop filtering product
          & Q(subcategory_id__main_cat__name__icontains=category)
          & Q(admin_status = True)
          & Q(active = True))
         
        elif subcategory is not None:
         products = Products.objects.filter(
          Q(price__range=(int(price), int(price) + 200)) 
          & Q(subcategory_id__sub_name__icontains=category)
          & Q(admin_status = True)
          &Q(active = True))
         
        else:
            products = Products.objects.filter(
            Q(price__range=(int(price), int(price) + 200))
            & Q(admin_status = True)
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
#closed
#single product details views
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def single_product(request,product_id,wishlist):
    user=get_object_or_404(User,id=request.user.id)
    customer=get_object_or_404(Customer_profile,customer_id=user.id)
    product = get_object_or_404(Products,id = product_id)
    category = Products.objects.filter(subcategory_id = product.subcategory_id)
  
    if wishlist!=0:
        print('inside the wishlist')
        try:
              product = get_object_or_404(Products, id=wishlist)
              wishlist_item = Wishlist.objects.filter(product=product,customer=customer)
              if wishlist_item.exists():
                  print('product is in the wishlist')
                  messages.success(request, "Product already in the wishlist")
                  return redirect('customer:single_product',product_id,0)
              else:
                  user = get_object_or_404(User, id=request.user.id)
                  customer = get_object_or_404(Customer_profile, customer_id=user)
                  new_wishlist = Wishlist(customer=customer, product=product)
                  new_wishlist.save()
                  messages.success(request, "Product added to wishlist")
        except Exception as e:
                 messages.error(request, f"Invalid request ")
                 return redirect('customer:single_product',product_id,0)
    context={
      'product' : product ,
      'category' : category
    }
    return render(request,'customer/single_product.html',context)
 
 # add to cart
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def add_to_cart(request,product_id):
    product = get_object_or_404(Products,id=product_id)
    user=get_object_or_404(User,id=request.user.id)
    customer=get_object_or_404(Customer_profile,customer_id=user.id)
    if request.method == "POST":
        quantity = request.POST.get('value')
        if Cart.objects.filter(customer_id=customer,product_id=product).exists():
             messages.error(request,'Same product exists in the cart ,Go to to the cart and update') 
             return redirect('customer:single_product',product_id,0)
        if int(quantity )<6:
         cart_offer=(product.price) - (product.subcategory_id.main_cat.offer_price)
         if product.offer_price == 0:
            offer_price= product.price
         else:
             offer_price=product.offer_price
         if offer_price<=cart_offer and product.offer_price >0:
             price=product.offer_price
             cart_offer=0
             product_offer=price
             print('offer_price')
         elif offer_price>=cart_offer and cart_offer >0 :
             price=cart_offer
             product_offer=0
             cart_offer=product.subcategory_id.main_cat.offer_price
             print('cat_price')
         else:
             price=product.price 
             cart_offer=0
             product_offer=0
             print('normal_price')
         cart = Cart(customer_id=customer,product_price=price,cat_offer=cart_offer,product_offer=product_offer,product_id=product,total_quantity=quantity)
         cart.save()
         messages.success(request,'product add to cart') 
        else:
          messages.error(request,'You cannot buy more than 5 same product') 
        return redirect('customer:single_product',product_id,0)
    else:
      return redirect('customer:single_product',product_id,0)  
 # cart view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def view_cart(request,product_id,wishlist):
    user=get_object_or_404(User,id=request.user.id)
    customer= get_object_or_404(Customer_profile,customer_id=user)
    try:
       cart_products = Cart.objects.filter(customer_id=customer).annotate(
       total_price=Sum(F('total_quantity') * F('product_price')))
       
       if not cart_products.exists():
        cart_products = 0  
        messages.error(request, 'No products added to the cart.')
    except Cart.ObjectDoesNotExist:
        messages.error(request,'No product added to cart') 
    if wishlist!=0:
        product=get_object_or_404(Products,id=wishlist)
        wishlist=Wishlist(customer=customer,product=product)
        wishlist.save()
        messages.success(request,"Product add to wishlist")
    if cart_products != 0:
      if product_id > 0 :
         cart=get_object_or_404(Cart,id = product_id)
         cart.delete()
         messages.success(request,'delete product from cart') 
    if cart_products != 0:
      all_total_price = cart_products.aggregate(all_total=Sum('total_price'))
    else:
        all_total_price=0
    context={
        'cart_products':cart_products,
        'all_total_price':all_total_price,
        'customer':customer
    }
    return render(request,'customer/cart.html',context)
 #cart quantity update
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def update_quantity_in_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = request.POST.get('quantity')
        update_product = get_object_or_404(Cart,id=product_id)
        if int(new_quantity) < 6 and int(new_quantity)>0:
           update_product.total_quantity = int(new_quantity)
           update_product.save()
           messages.success(request,'product quantity updated')
        else:
           messages.error(request,'You cannot buy more than 5 same product')  
        return redirect('customer:view_cart',0,0)
    else:
        return redirect('customer:view_cart',0,0)
    
# checkout multiple products   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def all_products_checkout(request):
    cart_id=0
    user = get_object_or_404(User,id=request.user.id)
    customer = get_object_or_404(Customer_profile,customer_id=user.id)
    address=customer_address.objects.filter(user_id=customer)
    if address.exists():
        customer_current_address=address.filter(current='YES')
    else:
         messages.error(request,'You have no address,add an current address')
         return redirect('customer:customerProfile')
    cart_products=Cart.objects.filter(customer_id=customer.id,product_id__quantity__gt = 0).annotate(
        total_price=F('total_quantity') * F('product_price'))
    if cart_products.exists():
      total_price = cart_products.aggregate(total=Sum('total_price'))
      total_price=total_price['total'] + 50
      coupons=Coupon.objects.filter(min_buy_price__lt=total_price,quantity__gt=0)
    else:
         return redirect('customer:shop',0) 
    status='all_products_checkout'
    amount=total_price-50
    
    context={
        'cart_products' : cart_products,
        'customer_current_address' : customer_current_address,
        'total_price':total_price,
        'address':address,
        'status':status,
        'cart_id':cart_id,
        "coupons":coupons,
    }
    return render(request,'customer/checkout.html',context)

#checkout single product
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def single_product_checkout(request,cart_id):
     user = get_object_or_404(User,id=request.user.id)
     customer = get_object_or_404(Customer_profile,customer_id=user.id)
     address=customer_address.objects.filter(user_id=customer)
     if address.exists():
        customer_current_address=address.filter(current='YES')
     else:
         messages.error(request,'You have no address,add an current address')
         return redirect('customer:customerProfile')
     cart_products=Cart.objects.filter(id=cart_id).annotate(
        total_price=F('total_quantity') * F('product_price'))
     if cart_products.exists():
       total_price = cart_products.aggregate(total=Sum('total_price'))
       total_price=total_price['total'] + 50
       coupons=Coupon.objects.filter(min_buy_price__lt=total_price,quantity__gt=0)
     else:
         return redirect('customer:shop',0) 
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
         "coupons":coupons,
        
     }
     return render(request,'customer/checkout.html',context)
 
 # checkout address
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
  
# place order view 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')  
def place_order(request,cart_id,status):
    if request.method == 'POST':
        user = get_object_or_404(User,id=request.user.id)
        customer = get_object_or_404(Customer_profile,customer_id=user.id)
        address = get_object_or_404(customer_address,user_id = customer.id,current='YES')
        paymethod = request.POST.get('paymentMethod')
        coupon_id = request.POST.get('coupon_id')
        print(coupon_id)
        if coupon_id:
            couponid=coupon_id.strip()
            try:
              coupon =get_object_or_404(Coupon,coupon_id=couponid)     # coupon 
            except Http404:
                messages.error(request,'Coupon is Invalid!')
                return redirect('customer:place_order',cart_id,status)
            coupon_price= coupon.offer_price
            couponID=coupon.coupon_id
            try:
             user_order =Order.objects.filter(customer=customer,coupon_id=couponid)
             user_used=user_order.aggregate(count=Count('id'))
             user_quantity = user_used['count']
            except ObjectDoesNotExist:
                user_quantity=0
            if coupon.quantity <=user_quantity:
               if status=="single_product_checkout":
                   messages.error(request,'Coupon cannot applied, limit over!')
                   return redirect('customer:single_product_checkout',cart_id)
               else:
                   messages.error(request,'Coupon cannot applied, limit over!')
                   return redirect('customer:all_products_checkout')
        else:
            coupon_price=0
            couponID='NULL'      
        if int(paymethod) == 3: # cash on delivery
            amount=0
            if status == 'single_product_checkout':# single product
                carts = get_object_or_404(Cart,id = cart_id)
                if carts.product_id.quantity > 0 and carts.total_quantity <= carts.product_id.quantity :
                  if carts:
                    order=Order(customer=customer,vendor=carts.product_id.seller_id,
                              product=carts.product_id,delivery_address=address.addres,
                              coupon_id=couponID,coupon_price=coupon_price,
                              cat_offer=carts.cat_offer,product_offer=carts.product_offer,
                              pincode=address.pincode,phone_number=address.phone_number,
                              total_amount=carts.total_quantity*(carts.product_price-coupon_price),
                              quantity=carts.total_quantity
                              )
                    if order.total_amount <= 1000:
                        order.save()
                        payment=Payment(user=customer,transaction_id=0,
                               amount=order.total_amount,status="done",
                               vendor=carts.product_id.seller_id,payment_category='cash_on_delivery'
                               )
                        payment.save()
                        order.Payment=payment
                        order.save()
                        product = get_object_or_404(Products,id=carts.product_id.id)
                        product.quantity = (product.quantity) - (carts.total_quantity)
                        product.save()
                        carts.delete()
                    else:
                      messages.success(request,'You cannot buy products above 1000/Rs through cash on delivery.Choose other payment option' )
                      return redirect('customer:view_cart',0,0)      
                  else:
                    return redirect('c_home')
                else:
                    messages.success(request,f'Cannot buy product{carts.product_id.product_name},Because product has no this much quantity,You can buy below {carts.product_id.quantity}')
                    return redirect('customer:view_cart',0,0)  
            elif status == 'all_products_checkout':#multiple products
               amount=0
               carts = Cart.objects.filter(customer_id=customer.id)
               print(carts)
               if carts.exists():
                 count=carts.aggregate(count=Count('id'))
                 if coupon_price>0:
                    count=count['count']
                    price=coupon_price/count
                 else:
                     price=0
                 for cart in carts:
                     amount=amount+(cart.total_quantity*(cart.product_price-price))
                 if amount <= 1000: 
                    for cart in carts:
                     if cart.product_id.quantity > 0 and cart.total_quantity <= cart.product_id.quantity :
                       order=Order(customer=customer,vendor=cart.product_id.seller_id,
                                coupon_id=couponID,coupon_price=price,   
                                product=cart.product_id,delivery_address=address.addres,
                                cat_offer=cart.cat_offer,product_offer=cart.product_offer,
                                pincode=address.pincode,phone_number=address.phone_number,
                                total_amount=cart.total_quantity*(cart.product_price-price),
                               quantity=cart.total_quantity
                              )
                       order.save()
                       payment=Payment(user=customer,transaction_id=0,
                               amount=order.total_amount,status="no",
                               vendor=cart.product_id.seller_id,payment_category='cash_on_delivery'
                               )
                       payment.save()
                       order.Payment=payment
                       order.save()
                       product = get_object_or_404(Products,id=cart.product_id.id)
                       product.quantity = (product.quantity) - (cart.total_quantity)
                       product.save()
                       cart.delete()
                     else:
                       messages.success(request,f'Cannot buy product{cart.product_id.product_name},Because product has no this much quantity,You can buy below {cart.product_id.quantity}') 
                 else:
                   messages.success(request,'You cannot buy products above 1000/Rs through cash on delivery.Choose other payment option' )
                   return redirect('customer:view_cart',0,0)         
               else:
                return redirect('c_home')
        current_time =  timezone.now().replace(microsecond=0)
        order_products=Order.objects.filter(created_at = current_time,customer=customer)
        total_amount =order_products.aggregate(total=Sum('total_amount')) 
        if int(paymethod) == 1 :#online payment
            if status == 'single_product_checkout':# single product
                carts = get_object_or_404(Cart,id = cart_id)
                if carts.product_id.quantity > 0 and carts.total_quantity <= carts.product_id.quantity :
                 if carts:
                    order=Order(customer=customer,vendor=carts.product_id.seller_id,
                              product=carts.product_id,delivery_address=address.addres,
                              coupon_id=couponID,coupon_price=coupon_price,
                              cat_offer=carts.cat_offer,product_offer=carts.product_offer,
                              pincode=address.pincode,phone_number=address.phone_number,
                              total_amount=carts.total_quantity*(carts.product_price-coupon_price),
                              quantity=carts.total_quantity
                              )
                    order.save()
                    current_time =  order.created_at
                    product = get_object_or_404(Products,id=carts.product_id.id)
                    product.quantity = (product.quantity) - (carts.total_quantity)
                    product.save()
                    carts.delete()
                    return redirect('customer:rasorpay',order.id,status)
                 else:
                    return redirect('c_home')
                else:
                    messages.success(request,f'Cannot buy product{carts.product_id.product_name},Because product has no this much quantity,You can buy below {carts.product_id.quantity}')
                    return redirect('customer:view_cart',0,0)  
            elif status == 'all_products_checkout':# all product 
              carts = Cart.objects.filter(customer_id=customer.id)
              if carts.exists:
                 object_count=0
                 count=carts.aggregate(count=Count('id'))
                 if coupon_price>0:
                   count=count['count']
                   price=coupon.offer_price/count
                 else:
                     price=0
                 for cart in carts:
                  if cart.product_id.quantity > 0 and cart.total_quantity <= cart.product_id.quantity :
                     order=Order(customer=customer,vendor=cart.product_id.seller_id,
                              product=cart.product_id,delivery_address=address.addres,
                              coupon_id=couponID,coupon_price=price,
                              cat_offer=cart.cat_offer,product_offer=cart.product_offer,
                              pincode=address.pincode,phone_number=address.phone_number,
                              total_amount=cart.total_quantity*(cart.product_price-price),
                              quantity=cart.total_quantity
                              )
                     order.save()
                     product = get_object_or_404(Products,id=cart.product_id.id)
                     product.quantity = (product.quantity) - (cart.total_quantity)
                     product.save()
                     cart.delete()
                  object_count+=1
                 if len(carts) == object_count:
                  return redirect('customer:rasorpay',order.id,status,'None')
              else:
                 return redirect('c_home')
        if int(paymethod) == 2: #wallet
          Wallet=wallet.objects.filter(customer=customer)
          if Wallet.exists():
            refund_amount=wallet.objects.filter(customer=customer,status='refund').aggregate(amount=Sum('total_amount'))
            if refund_amount['amount'] == None:
               refund_amount['amount'] = 0
            paid_amount=wallet.objects.filter(customer=customer,status='paid').aggregate(amount=Sum('total_amount'))
            if paid_amount['amount'] == None:
               paid_amount['amount'] = 0
            wallet_amount=refund_amount['amount']-paid_amount['amount']
            if status == 'single_product_checkout':
                  carts = get_object_or_404(Cart,id = cart_id)  
                  cart_total=carts.total_quantity*(carts.product_price-coupon_price)
                  if cart_total <= wallet_amount:
                    if carts.product_id.quantity > 0 and carts.total_quantity <= carts.product_id.quantity :
                     if carts:
                       order=Order(customer=customer,vendor=carts.product_id.seller_id,
                              product=carts.product_id,delivery_address=address.addres,
                              coupon_id=couponID,coupon_price=coupon_price,
                              cat_offer=carts.cat_offer,product_offer=carts.product_offer,
                              pincode=address.pincode,phone_number=address.phone_number,
                              total_amount=carts.total_quantity*(carts.product_price-coupon_price),
                              quantity=carts.total_quantity
                              )
                       order.save()
                       Wallet=wallet(customer=order.customer,vendor=order.vendor,product=order.product,total_amount=order.total_amount,status='paid')
                       Wallet.save()
                       payment=Payment(user=customer,transaction_id=1,
                               amount=order.total_amount,status="done",
                               vendor=carts.product_id.seller_id,payment_category='Wallet'
                               )
                       payment.save()
                       order.Payment=payment
                       order.save()
                       product = get_object_or_404(Products,id=carts.product_id.id)
                       product.quantity = (product.quantity) - (carts.total_quantity)
                       product.save()
                       carts.delete()
                     else:
                       return redirect('c_home')
                    else:
                      messages.success(request,f'Cannot buy product{carts.product_id.product_name},Because product has no this much quantity,You can buy below {carts.product_id.quantity}')
                      return redirect('customer:view_cart',0,0)  
                  else: 
                      messages.error(request," Wallet have no amount than product amount")
                      return redirect('customer:single_product_checkout',cart_id)
            elif status == 'all_products_checkout':
               carts = Cart.objects.filter(customer_id=customer.id)
               if carts.exists:
                 count=carts.aggregate(count=Count('id'),amount=Sum('product_price'))
                 for cart in carts:
                     cart_total=cart
                 if coupon_price>0:
                    count=count['count']
                    price=coupon_price/count
                 else:
                     price=0
                 for cart in carts:
                    cart_total=cart.total_quantity*(cart.product_price-price)
                 if int(cart_total)<=wallet_amount:
                   for cart in carts:
                    if cart.product_id.quantity > 0 and cart.total_quantity <= cart.product_id.quantity :
                     order=Order(customer=customer,vendor=cart.product_id.seller_id,
                                coupon_id=couponID,coupon_price=price,   
                                product=cart.product_id,delivery_address=address.addres,
                                cat_offer=cart.cat_offer,product_offer=cart.product_offer,
                                pincode=address.pincode,phone_number=address.phone_number,
                                total_amount=cart.total_quantity*(cart.product_price-price),
                               quantity=cart.total_quantity
                              )
                     order.save()
                     Wallet=wallet(customer=order.customer,vendor=order.vendor,product=order.product,total_amount=order.total_amount,status='paid')
                     Wallet.save()
                     payment=Payment(user=customer,transaction_id=1,
                               amount=order.total_amount,status="done",
                               vendor=cart.product_id.seller_id,payment_category='Wallet'
                               )
                     payment.save()
                     order.Payment=payment
                     order.save()
                     product = get_object_or_404(Products,id=cart.product_id.id)
                     product.quantity = (product.quantity) - (cart.total_quantity)
                     product.save()
                     cart.delete()
                     
                 else:
                    messages.error(request," Wallet have no amount than product amount")  
                    return redirect('customer:all_products_checkout')
               else:
                      return redirect('c_home')
            current_time =  timezone.now().replace(microsecond=0)
            order_products=Order.objects.filter(created_at = current_time,customer=customer)
            total_amount =order_products.aggregate(total=Sum('total_amount')) 
          else:
            if status =='all_products_checkout':
                 messages.error(request," No Wallet ")  
                 return redirect('customer:all_products_checkout') 
            elif status =='single_product_checkout':
                 messages.error(request," No Wallet ")
                 return redirect('customer:single_product_checkout',cart_id)   
           
        context={
        'order_products' : order_products,
        'total_amount': total_amount,
        'payment':payment,
        'order':order,
        }
      
        return render(request,'customer/place_order.html',context)
    
#rasorpay
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def rasorpay(request,order_id,status,state):
    orders=get_object_or_404(Order,id=order_id)
    if orders.Payment:
        return redirect('customer:shop',0)
    else:
     if status =='single_product_checkout':
        orders=get_object_or_404(Order,id=order_id)
        amount=orders.total_amount+50
        amount_in_paise = int(amount) * 100  
        currency="INR"
        order=razorpay_client.order.create(
        {
                "amount": amount_in_paise,
                "currency": currency,
                "payment_capture": "1"
               
            }
           )
     if status == 'all_products_checkout':
        user = get_object_or_404(User,id=request.user.id)
        customer = get_object_or_404(Customer_profile,customer_id=user.id)
        order=get_object_or_404(Order,id=order_id)
        current_time=order.created_at
        orders = Order.objects.filter(customer=customer,created_at=current_time)
        total_amount = orders.aggregate(total=Sum('total_amount'))
        amount = total_amount['total']+int(50)
        amount_in_paise = int(amount) * 100 
        currency="INR"
        order=razorpay_client.order.create(
        {
                "amount":amount_in_paise ,
                "currency": currency,
                "payment_capture": "1"  
            }
           )
    context={
        "order_id": order["id"],
        "amount": amount,
        "key_id": settings.RAZORPAY_KEY_ID,
         "order" :order_id,
         "status":state
        }
    return render(request,'customer/rasorpay.html',context)

#rasorpay payment verification
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def verify_payment(request,order_id,status):
    if request.method == 'POST':
        user=get_object_or_404(User,id=request.user.id)
        customer=get_object_or_404(Customer_profile,customer_id=user)
        order=get_object_or_404(Order,id=order_id)
        current_time=order.created_at
        orders = Order.objects.filter(customer=customer,created_at=current_time)
        try:
            data = json.loads(request.body)
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_signature = data.get('razorpay_signature')
            
            # Verify the signature
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            if status =='payment_failed':
               order=get_object_or_404(Order,id=order_id)
               vendor=get_object_or_404(Vendor_profile,id=order.vendor.id)
               payment=Payment(user=customer,transaction_id=razorpay_payment_id,
                               amount=order.total_amount,status="done",
                               vendor=vendor,payment_category='online_payment'
                               )
               payment.save()
               order.Payment=payment
               order.save()
                
            else: 
             for order in orders:
               vendor=get_object_or_404(Vendor_profile,id=order.vendor.id)
               payment=Payment(user=customer,transaction_id=razorpay_payment_id,
                               amount=order.total_amount,status="done",
                               vendor=vendor,payment_category='online_payment'
                               )
               payment.save()
               order.Payment=payment
               order.save()
              
            # Success response
            return JsonResponse({"message": "Payment verified successfully!"})

        except SignatureVerificationError as e:
            print(f"Signature Verification Error: {str(e)}")
            return JsonResponse({"message": "Payment verification failed!"}, status=400)
        except Exception as e:
            print(f"Other Error: {str(e)}")
            return JsonResponse({"message": "An error occurred!"}, status=500)

# rasorpay place order 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')        
def rasorpay_order_status(request,order_id,state):
    user=get_object_or_404(User,id = request.user.id)
    customer=get_object_or_404(Customer_profile,customer_id=user)
   
    if state == 'payemnt_failed':
       order_products = get_object_or_404(Order,id=order_id) 
       payment=get_object_or_404(Payment,payment_id=order_products.Payment.payment_id) 
       total_amount=order_products.total_amount
       order=order_products
    else:
      order = get_object_or_404(Order,id=order_id)
      current_time=order.created_at
      order_products=Order.objects.filter(created_at =current_time,customer=customer)
      payment=get_object_or_404(Payment,payment_id=order.Payment.payment_id)
      total_amount =order_products.aggregate(total=Sum('total_amount'))
    status='rasorpay'
    context={
        'order_products' : order_products,
        'total_amount': total_amount,
        'status':status,
        'order':order,
        'payment':payment,
        'order_id':order_id
        }
    return render(request,'customer/place_order.html',context)
 
 # order history
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
#order cancel
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def order_cancel(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    product = get_object_or_404(Products,id=order.product.id)
    if order.Payment.payment_category == 'online_payment':
        payment_status=get_object_or_404(Payment,payment_id=order.Payment.payment_id)
        order.order_status = 'Cancelled'
        payment_status.status='refund'
        payment_status.save()
        Wallet=wallet(customer=order.customer,vendor=order.vendor,product=product,total_amount=order.total_amount,status='refund')
        Wallet.save()
        order.save() 
    elif order.Payment.payment_category == 'cash_on_delivery' :
        payment_status=get_object_or_404(Payment,payment_id=order.Payment.payment_id)
        order.order_status = 'Cancelled'
        payment_status.status='no'
        payment_status.save()
        Wallet=wallet(customer=order.customer,vendor=order.vendor,product=product,total_amount=order.total_amount,status='refund')
        Wallet.save()
        order.save() 
    elif order.Payment.payment_category == 'Wallet':
        payment_status=get_object_or_404(Payment,payment_id=order.Payment.payment_id)
        order.order_status = 'Cancelled'
        payment_status.status='refund'
        payment_status.save()
        Wallet=wallet(customer=order.customer,vendor=order.vendor,product=product,total_amount=order.total_amount,status='refund')
        Wallet.save()
        order.save()  
    product.quantity = product.quantity + order.quantity
    product.save()
    messages.success(request,'Order is cancelled')
    return redirect('customer:order_history')
# search product 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def search_product(request):
  try:
    if request.method == 'POST':
        search = request.POST.get('search')
        products = Products.objects.filter(product_name__icontains=search,admin_status = True,active=True )
    else:
        product=[]
  except Exception:
       products=[]
       messages.error(request,'product is not available')
     
  return render(request,'customer/shop.html',{'products':products})
# Wallet  view
def My_wallet(request):
    user=get_object_or_404(User,id=request.user.id)
    customer=get_object_or_404(Customer_profile,customer_id = user)
    wall=wallet.objects.filter(customer=customer)
    if wall.exists():
       try:
        refund_amount=wall.filter(status='refund').aggregate(total=Sum('total_amount'))
       except Exception:
           refund_amount['total']=0
       try:
         paid_amount=wall.filter(status='paid').aggregate(total=Sum('total_amount'))
       except Exception:
           paid_amount['total']=0
       if paid_amount['total'] == None:
             amount=refund_amount['total']
       else:
           amount=refund_amount['total']-paid_amount['total'] 
    else:
      wall=0 
      amount=0
    if amount < 1:
        amount=0
    context={
     "wallet":wall ,
     "total_amount":amount
    }
    return render(request,'customer/wallet.html',context)

# return product
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def return_product(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    if order.order_status == 'Return' or order.order_status == 'Returned':
        return redirect('customer:order_history')
    if request.method == 'POST':
        reason=request.POST.get('reason')
        ret=Return_product(customer=order.customer,order=order,reason=reason)
        ret.save()
        messages.success(request,'product return successfully')
        order.order_status ='Return'
        order.save()
        return redirect('customer:order_history')
    context={
        'order':order
    }
    return render(request,'customer/return.html',context)
#wishlist
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def wishlist(request,product):
    user=get_object_or_404(User,id=request.user.id)
    customer=get_object_or_404(Customer_profile,customer_id = user)
    products=Wishlist.objects.filter(customer=customer)
    if product > 0:
        product=get_object_or_404(Wishlist,id=product)
        product.delete()
        messages.success(request,'delete product from wishlist')
    context={
        "products":products
    }
    return render(request,'customer/whislist.html',context)

#invoice pdf
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def invoice_pdf_view(request,order_id):
    user = get_object_or_404(User,id=request.user.id)
    customer=get_object_or_404(Customer_profile,customer_id=user)
    order = get_object_or_404(Order,id=order_id)
    current_time=order.created_at
    order_products=Order.objects.filter(created_at =current_time,customer=customer)
    total_amount =order_products.aggregate(total=Sum('total_amount'))
    print(f'order_product:{order_products}')
    payment=get_object_or_404(Payment,payment_id=order.Payment.payment_id)
    print(f'payment:{payment}')
    # Render the HTML template with context
    context = {'order_products': order_products,'payment':payment,'customer':customer,'order':order,'total_amount':total_amount}
    html_content = render_to_string('customer/invoice.html', context)
    
    PDFKIT_OPTIONS = {
    'page-size': 'A4',
    'encoding': 'UTF-8',
    'no-outline': None
     }
    # Generate the PDF
    pdf = pdfkit.from_string(html_content, False,configuration=PDFKIT_CONFIG, options=PDFKIT_OPTIONS)

    # Return the PDF as a downloadable file
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoicePdf.pdf"'

    return response
    
