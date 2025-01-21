from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.cache import cache_control
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login,logout as authlogout
from django.shortcuts import get_object_or_404
from .models import *
from django.db.models import F, Sum,Count
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models.functions import ExtractYear,ExtractWeek, ExtractWeekDay
import datetime
from customer.models import *
from .forms import *
from .utils import *
import json

def is_user(user):
    return user.is_authenticated == False
 
#@user_passes_test(is_user)
def index(request):
    if request.user.is_authenticated and request.user.Role == 1:  
      return redirect('c_home',0)
    elif request.user.is_authenticated and request.user.Role == 2:
      return redirect('v_home')                                     
    elif request.user.is_authenticated and request.user.is_admin:
      return redirect('admin_home')
    else:
      trusted_brands=Products.objects.values('brand_name').distinct('brand_name')
      top_products=Products.objects.annotate(count=Count('order')).order_by('-count')[:5]
      # latest_products=Products.objects.all().order_by('-created_at')[:5]
      # print(latest_products)
      context={
       'trusted_brands':trusted_brands,
       'top_products':top_products
      }
      return render(request,'index.html',context)
  
  
# <--------admin side funtions---------->

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Admin_login(request):
  if request.user.is_authenticated and request.user.Role == 1:  
      return redirect('c_home',0)
  elif request.user.is_authenticated and request.user.Role == 2:
      return redirect('v_home')                                     
  elif request.user.is_authenticated and request.user.is_admin:
      return redirect('admin_home')
  form = customerLogin() 
  if request.method == 'POST':
      form = customerLogin(request.POST)
      if form.is_valid():
            email = form.cleaned_data.get('email_id')
            password = form.cleaned_data.get('password')
            admin=authenticate(email=email, password=password)
            if admin is not None:
              if admin.is_admin:
                  login(request, admin)
                  return redirect('admin_home') 
              else:
                messages.error(request," not valid admin !")   
            else:
              messages.error(request," please enter correct email id and password !")
      else:
          messages.error(request," please enter correct email id and password !")
  else:
         form = customerLogin() 
  return render(request,'custom_admin/login.html',{'form':form})

# closed signup
#admin home
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def Admin_home_page(request):
   total_customer=Customer_profile.objects.all().aggregate(count=Count('id'))
   total_vendor=Vendor_profile.objects.all().aggregate(count=Count('id'))
   total_Products=Products.objects.all().aggregate(count=Count('id'))
   sales_count=Order.objects.filter(Payment__status='done').count()
   sales_amount=Order.objects.filter(Payment__status='done').aggregate(total=Sum('total_amount'))
   coupon_discount=Order.objects.filter(Payment__status='done').aggregate(discount=Sum('coupon_price'))
   
# top
   top_products=Products.objects.annotate(count=Count('order')).order_by('-count')[:10]
   top_category=Products.objects.values('subcategory_id__main_cat__name').annotate(count=Count('order')).order_by('-count')[:10]
   top_brand=Products.objects.values('brand_name').annotate(count=Count('order')).order_by('-count')[:10]
   top_vendors=Order.objects.filter(Payment__status='done').values('vendor__seller_name').annotate(count=Count('id'),amount=Sum('total_amount')).order_by('-count')[:3]
   
#graph----------------------->
   years=[]
   years_orders=[]
   Months_order=[]
   week_orders=[]
   today = datetime.today()
   # year and orders
   years_objects = Order.objects.annotate(year=ExtractYear('created_at')).values_list('year', flat=True).distinct().order_by('year')
   for year in years_objects:
        years.append(str(year))
   for year in years:
       order_number=Order.objects.filter(created_at__year=int(year)).count()
       years_orders.append(order_number)
   #closed
   #month and orders
   months = [1,2,3,4,5,6,7,8,9,10,11,12]
   for month in months:
        order_number=Order.objects.filter(created_at__year=today.year,created_at__month=month,).count()
        Months_order.append(order_number)
   #closed
   #week and orders 
   weeks=[1,2,3,4,5,6,7]
   week_no=today.isocalendar()[1]
   for week in weeks:
       order_number=Order.objects.annotate(week=ExtractWeek('created_at'),weekday=ExtractWeekDay('created_at')).filter(created_at__year=today.year,created_at__month=today.month,week=week_no,weekday=week).count()
       week_orders.append(order_number)
   #closed
#graph_----------closed>
  
   context={
      'total_customers':total_customer['count'],
      'total_vendors':total_vendor['count'],
      'total_products':total_Products['count'],
      'sales_count': sales_count,
      'sales_amount':sales_amount['total'],
      'coupon_discount':coupon_discount['discount'],
      'top_products':top_products,
      'top_category':top_category,
      'top_brands':top_brand,
      'top_vendors':top_vendors,
      
      'years':json.dumps(years),
      'years_orders':json.dumps(years_orders),    # graph data
      'Months_order':json.dumps(Months_order),
      'week_orders':json.dumps(week_orders),
   }
   return render(request,'custom_admin/home.html',context)
# closed admin home 
# admin customer side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def Customer_side(request):
   if request.method=='POST':
      name=request.POST.get('search')
      customer=Customer_profile.objects.filter(full_name__icontains=name)
   else:
      customer=Customer_profile.objects.all() 
      if customer == None:
       messages.error(request," No customers found !")
      else:
       customer=customer
   context = {
      'customer': customer
      }
   return render(request,'custom_admin/custmor.html',context)
# closed admin customer side
# admin side customer blocked
@login_required(login_url='admin_log')
def Block_customer(request,user_id):
      customer=get_object_or_404(User,id=user_id)
      customer.is_active=False
      customer.save()
      return redirect('customer_side')
# closed
# admin side customer unblocked
@login_required(login_url='admin_log')
def UnBlock_customer(request,user_id):
      customer=get_object_or_404(User,id=user_id)
      customer.is_active=True
      customer.save()
      return redirect('customer_side')
#closed
# admin vender side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def Vendor_side(request):
   if request.method=='POST':
      name=request.POST.get('search')
      vendor=Vendor_profile.objects.filter(seller_name__icontains=name)
   else:
       vendor=Vendor_profile.objects.all()
       if vendor == None:
         messages.error(request," No vendors found !")
       else:
          vendor=vendor
   context = {
      'vendor': vendor
       }
   return render(request,'custom_admin/vendor.html',context)
# closed
#vendor details
@login_required(login_url='admin_log')
def vendor_details(request,vendor_id):
   vendor=get_object_or_404(Vendor_profile,id=vendor_id)
   product_count=Products.objects.filter(seller_id=vendor).count()
   blocked_product=Products.objects.filter(seller_id=vendor,admin_status=False).count()
   context={
      'vendor':vendor,
      'product_count':product_count,
      'blocked_product':blocked_product
   }
   return render(request,'custom_admin/vendordetails.html',context)

#closed
# admin vender blocked
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def Block_vendor(request,user_id):
      vendor=get_object_or_404(User,id=user_id)
      vendor.is_active=False
      vendor.save()
      return redirect('vendor_side')
#closed
#admin side vendor unblocked
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def UnBlock_vendor(request,user_id):
      vender=get_object_or_404(User,id=user_id)
      vender.is_active=True
      vender.save()
      return redirect('vendor_side')
#closed
#admin side vendor approval
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def vender_approval(request,user_id):
      vender=get_object_or_404(Vendor_profile,id=user_id)
      vender_user=get_object_or_404(User,id=vender.vendor_id.id)
      context={
         'vender':vender,
         'vender_user':vender_user
      }
      return render(request,'custom_admin/vendor_approve.html',context)
#closed
 #admin side vendor approved
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@login_required(login_url='admin_log')
def vender_approved(request,user_id):
      vendor=get_object_or_404(Vendor_profile,id=user_id)
      vender_user=get_object_or_404(User,id=vendor.vendor_id.id)
      if approval_email(vender_user,text=None):
         vender_user.is_active = True
         vender_user.save() 
         return redirect('vendor_side')
    #closed 
#admin side vendor not approved
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')   
def novender_approved(request,user_id):
      vendor=get_object_or_404(Vendor_profile,id=user_id)
      user=vendor.vendor_id
      if request.method == 'POST':
        text=request.POST.get('email')
        if approval_email(user,text):
          return redirect('vendor_side')
#closed

# admin product category
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def category(request):
   categories=Category.objects.all()
   if categories is None:
      messages.error(request," No categories found !")
   if request.method=='POST':
      form = CategoryForm(request.POST)
      if form.is_valid():
         try:
           form.save()
         except IntegrityError:
            messages.error(request,"Not add existing category!")
         return redirect('category')
   else:
      form = CategoryForm()
   context={
      'categories':categories,
      'form':form
   }
   return render(request, 'custom_admin/category.html',context)
#closed
# admin update categories
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def update_category(request,cat_id):
   category=get_object_or_404(Category,id=cat_id)
   if request.method == 'POST':
      name=request.POST.get('name')
      desc=request.POST.get('desc')
      offer_price=request.POST.get('offer')
      if float(offer_price)>= 0:
        category.name=name
        category.desc=desc
        category.offer_price=offer_price
        category.save()
        return redirect('category')
      else:
        messages.error(request,"please update offer price above,0") 
        return redirect('update_category',cat_id)
   return render(request,'custom_admin/update_category.html',{'category':category})
   #closed
# admin delete categories
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def delete_category(request,cat_id):
   category=get_object_or_404(Category,id=cat_id)
   category.delete = True
   category.save()
   return redirect('category')
#closed
#product listing 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def product_listing(request,product_id,status):
   vendors=Vendor_profile.objects.all().distinct()
   products=Products.objects.all()
   if product_id > 0 and status == "block":
      item=get_object_or_404(Products,id=product_id)
      item.admin_status=False
      item.save()
      messages.success(request,'Product Blocked')
   if product_id > 0 and status == "unblock":
      item=get_object_or_404(Products,id=product_id)
      item.admin_status=True
      item.save()
      messages.success(request,'Product UnBlocked')
   context={
      'vendors':vendors,
      'products':products
   }
   return render(request,'custom_admin/productlist.html',context)
#closed
# add coupon
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def coupon(request):
    coupons = Coupon.objects.all()
    if request.method == 'POST': 
       name=request.POST.get('name')
       id=request.POST.get('id')
       offer=request.POST.get('offer')
       min_price=request.POST.get('min_price')
       date=request.POST.get('date')
       quantity=request.POST.get('quantity')
       if not name: 
          messages.error(request,"Name is required.")
          return redirect('coupon',coupons)
       if not name.replace(' ', '').isalnum(): 
           messages.error(request,"Name can only contain letters, numbers, and spaces..")
           return redirect('coupon')

       if int(offer)>0 and int(min_price)>0 and int(quantity)>0 and int(date)>0:
        if int(min_price)>int(offer):
          coupon=Coupon(coupon_name=name,coupon_id =id,offer_price = offer, quantity=quantity, min_buy_price=min_price, validity_date=date)
          coupon.save()
          days=int(date)
          coupon.validity=coupon.created_at + timedelta(days=days)
          coupon.save()
          messages.success(request,"coupon created")
        else:
          messages.error(request,"Please enter the min price above than offer")
       else:
         messages.error(request,"Please enter in offer,min price,quantity and date above 0")
    return render(request,'custom_admin/cupon.html',{'coupons':coupons})
#delete coupon
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def delete_coupon(request,coupon_id):
   coupon = get_object_or_404(Coupon,id=coupon_id)
   coupon.delete()
   messages.success(request,"cupon deleted ")
   return redirect('coupon')

# <--------admin side funtions closed---------->

#<-------------------customer side funtions------------------->

# customer sign up
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Customer_sign_up(request):
  if request.user.is_authenticated and request.user.Role == 1:  
      return redirect('c_home',0)
  elif request.user.is_authenticated and request.user.Role == 2:
      return redirect('v_home')                                    
  elif request.user.is_authenticated and request.user.is_admin:
      return redirect('admin_home')               
  form = User_registretion()
  if request.method == 'POST':
      form = User_registretion(request.POST)
      if form.is_valid():
         user=form.save(role=1)
         if email(user.id):        #funtion call for email generation in utils.py
            return redirect('verify_otp',user.id,'none')
      else:
       messages.error(request,"please follow instructions  !")
       return render(request,'userRegistretion.html',{'form':form})
  else:
     form =User_registretion()
  return render(request,'userRegistretion.html',{'form':form})
#closed
# customer login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Customer_login(request):
   if request.user.is_authenticated and request.user.Role == 1:  
      return redirect('c_home',0)
   elif request.user.is_authenticated and request.user.Role == 2:
      return redirect('v_home')                                    
   elif request.user.is_authenticated and request.user.is_admin:
      return redirect('admin_home')
   if request.user.is_authenticated and request.user.Role == 1: 
      return redirect('c_home',0) 
   form = customerLogin()
   if request.method == 'POST':
      form = customerLogin(request.POST)
      if form.is_valid():
            email = form.cleaned_data.get('email_id')
            password = form.cleaned_data.get('password')
            try:
              user=User.objects.get(email=email)
              if user.is_active == False:
                messages.error(request," Admin blocked your access !")
                return redirect('c_login')
            except User.DoesNotExist:
               pass
            user = authenticate(email=email, password=password)
            if user is not None:
             if user.Role == 1 and user.is_active == True:
                login(request, user)
                return redirect('c_home',0)
             else:
               messages.error(request," Invalid customer !")  
            else:
              messages.error(request," please enter correct email id and password !")
      else:
          messages.error(request," please enter correct email id and password !")
   else:
         form = customerLogin() 
   return render(request,'c_login.html',{'form':form})
#closed
# customer home
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='c_login')
def Customer_home_page(request,product_id):
   if request.user.is_authenticated and request.user.Role == 2: 
         return redirect('v_home') 
   trusted_brands=Products.objects.values('brand_name').distinct('brand_name')
   top_products=Products.objects.annotate(count=Count('order')).order_by('-count')[:5]
      # latest_products=Products.objects.all().order_by('-created_at')[:5]
      # print(latest_products)
   if product_id > 0:
            product = get_object_or_404(Products, id=product_id)
            user = get_object_or_404(User, id=request.user.id)
            customer = get_object_or_404(Customer_profile, customer_id=user)
            try:
              wishlist_item = Wishlist.objects.get(product=product,customer=customer)
              if wishlist_item:
                  messages.success(request, "Product already in the wishlist")
                  return redirect('c_home', 0)
            except Wishlist.DoesNotExist:
             try:
                user = get_object_or_404(User, id=request.user.id)
                customer = get_object_or_404(Customer_profile, customer_id=user)
                new_wishlist = Wishlist(customer=customer, product=product)
                new_wishlist.save()
                messages.success(request, "Product added to wishlist")
             except Exception as e:
                 messages.error(request, f"An error occurred: {str(e)}")
                 return redirect('c_home', 0)
   context={
       'trusted_brands':trusted_brands,
       'top_products':top_products
      }
   return render(request,'customer/customer_home.html',context)
#closed
#<-------------------customer side funtions closed------------------->


#<-------------------vendor side funtions------------------->

#vendor sign-up
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Vender_sign_up(request):
  if request.user.is_authenticated and request.user.Role == 1:  
      return redirect('c_home',0)
  elif request.user.is_authenticated and request.user.Role == 2:
      return redirect('v_home')                                     
  elif request.user.is_authenticated and request.user.is_admin:
      return redirect('admin_home')
  form = User_registretion()
  vender=Vendor_license()
  if request.method == 'POST':
      form = User_registretion(request.POST)
      vender=Vendor_license(request.POST,request.FILES)
      print(form.is_valid())
      print(vender.is_valid())
      if form.is_valid() and vender.is_valid():
         user=form.save(role=2)
         print(user, user.full_name)
         if email(user.id):
            vender_instance = vender.save(commit=False)  
            vender_instance.vendor_id = user  
            vender_instance.seller_name = user.full_name  
            print(vender_instance.seller_name, vender_instance.vendor_id)
            vender_instance.save()  
            return redirect('verify_otp',user.id,'none')
      else:
          messages.error(request,"please follow instructions !")
  else:
       form = User_registretion()
       vender=Vendor_license()
  return render(request,'venderRegistretion.html',{'form':form,'vender':vender})
#closed
# vendor login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Vendor_login(request):
   if request.user.is_authenticated and request.user.Role == 1:  
      return redirect('c_home',0)
   elif request.user.is_authenticated and request.user.Role == 2:
      return redirect('v_home')                                    
   elif request.user.is_authenticated and request.user.is_admin:
      return redirect('admin_home')
   form = customerLogin()
   if request.method == 'POST':
      form = customerLogin(request.POST)
      if form.is_valid():
            email = form.cleaned_data.get('email_id')
            password = form.cleaned_data.get('password')
            try:
              user=User.objects.get(email=email)
              if user.is_active == False:
                messages.error(request," Admin blocked your access !")
                return redirect('v_login')
            except User.DoesNotExist:
               pass
            vendor=authenticate(email=email, password=password)
            if vendor is not None:
              if vendor.Role == 2 and vendor.is_active == True :
                login(request, vendor)
                return redirect('v_home') 
              else:
                messages.error(request," Invalid vendor !")
            else:
              messages.error(request," please enter correct email id and password !")
      else:
          messages.error(request," please enter correct email id and password !")
   else:
         form = customerLogin() 
   return render(request,'v_login.html',{'form':form})
#closed
#vender home
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='v_login')             
def Vendor_home_page(request):
    vendor = get_object_or_404(Vendor_profile, vendor_id=request.user.id)
    order_product = Order.objects.filter(vendor=vendor)
    customer_count = order_product.values('customer__id').distinct().aggregate(total=Count('customer__id'))
    products = Products.objects.filter(seller_id=vendor).aggregate(total=Count('id'))
    sale_products = order_product.filter(Payment__status='done')
    pending_orders = order_product.filter(order_status='Pending').aggregate(total=Count('id'))
    amount = sale_products.aggregate(sum=Sum('total_amount'), count=Count('id'))
    discount_amount = sale_products.annotate(
        discount=(F('product__price') * F('quantity')) - F('total_amount')
    )
    Total_discount_amount = discount_amount.aggregate(total_discount=Sum('discount'))
    total_discount_amount = Total_discount_amount['total_discount']
    sales_count = amount['count']
    total_sales_amount = amount['sum']

    # Top data
    top_products = Products.objects.filter(seller_id=vendor).annotate(
        total_sales=Count('order')
    ).order_by('-total_sales')[:10]
    top_brands = Products.objects.filter(seller_id=vendor).values(
        'brand_name'
    ).annotate(total_sales=Count('order')).order_by('-total_sales')[:10]
    top_customers = order_product.values('customer__full_name').annotate(
        total_order=Count('id')
    ).order_by('-total_order')[:10]
    
    #graph----------------------->
    years=[]
    years_orders=[]
    Months_order=[]
    week_orders=[]
    today = datetime.today()
    # year and orders
    years_objects = Order.objects.filter(vendor=vendor).annotate(year=ExtractYear('created_at')).values_list('year', flat=True).distinct().order_by('year')
    for year in years_objects:
        years.append(str(year))
    for year in years:
       order_number=Order.objects.filter(vendor=vendor,created_at__year=int(year)).count()
       years_orders.append(order_number)
   #closed
   #month and orders
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    for month in months:
        order_number=Order.objects.filter(vendor=vendor,created_at__year=today.year,created_at__month=month,).count()
        Months_order.append(order_number)
   #closed
   #week and orders 
    weeks=[1,2,3,4,5,6,7]
    week_no=today.isocalendar()[1]
    for week in weeks:
       order_number=Order.objects.annotate(week=ExtractWeek('created_at'),weekday=ExtractWeekDay('created_at')).filter(vendor=vendor,created_at__year=today.year,created_at__month=today.month,week=week_no,weekday=week).count()
       week_orders.append(order_number)
   #closed
   #graph_----------closed>
    context = {
        'sales_count': sales_count,
        'total_sales_amount': total_sales_amount,
        'Total_discount_amount': total_discount_amount,
        'total_products': products['total'],
        'total_customer': customer_count['total'],
        'pending_orders': pending_orders['total'],
        'top_products': top_products,
        'top_brands': top_brands,
        'top_customers': top_customers,
        
        'years':json.dumps(years),
        'years_orders':json.dumps(years_orders),    # graph data
        'Months_order':json.dumps(Months_order),
        'week_orders':json.dumps(week_orders),
    }
    return render(request, 'vendor/dashboard.html', context)

#closed

#<-------------------vendor side funtions closed------------------->

# ---------dependencies funtions -------------->
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def email_auth(request):
   if request.method == 'POST':
      mail=request.POST.get('email')
      try:
        user=User.objects.get(email=mail) 
      except User.DoesNotExist:
         messages.error(request,'Invalid email id ,Use proper email id..!')
         return redirect('email_auth')
      if user:
         if email(user.id):
           messages.success(request,'Enter otp for email authenication')
           return redirect('verify_otp',user.id,'forgot')
      else:
         messages.error(request,'Invalid email id ,Use proper email id..!')
         return redirect('email_auth')
   return render(request,'email_auth.html')

def forgot_password(request,user_id):
   user=get_object_or_404(User,id=user_id)
   if request.method == 'POST':
      password=request.POST.get('password')
      conform=request.POST.get('conform')
      print(password)
      print(conform)
      if password == conform:
         user.set_password(password)
         user.save()
         print('password changed')
         if user.Role == 1:
           messages.success(request,'password changed')
           return redirect('c_login')
         elif user.Role == 2:
           messages.success(request,'password changed')
           return redirect('v_login')
      else:
         messages.error(request,'Both passwords are not correct ..!')
         return redirect('forgot_password',user_id)
   return render(request,'forgot.html',{'user':user_id})
# verify otp
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otp_verify(request,user_id,status):
   if request.user.is_authenticated and request.user.Role == 1: 
      return redirect('c_home',0) 
   if request.user.is_authenticated and request.user.Role == 2: 
      return redirect('v_home') 
   user=get_object_or_404(User,id=user_id)
   if request.method == 'POST':
     user=get_object_or_404(User,id=user_id)
     try:
      n1=request.POST['n1']
      n2=request.POST['n2']
      n3=request.POST['n3']
      n4=request.POST['n4']
      n5=request.POST['n5']
      n6=request.POST['n6']
      otp=[n1,n2,n3,n4,n5,n6]
      single_number_otp = int("".join(map(str,otp)))
     except ValueError:
        messages.error(request," Please Enter correct otp !")
     except UnboundLocalError:
        messages.error(request," Please Enter correct otp !")   
     if verify_otp(single_number_otp,user.otp):#funtion call for verify otp in utils.py
        if status !='forgot':
          user.otp=None
          user.save()
        else:
          user.otp=None
          user.save()
          return redirect('forgot_password',user.id)
        if user.Role == 1:
           user.is_active=True
           user.save()
           return redirect('c_login')
        elif user.Role == 2:
           return redirect('v_login')
     else:
        messages.error(request," Please Enter correct otp !")
   return render(request,'otp_verify.html',{'user':user,'status':status})
#closed
# reset otp
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_otp(request,user_id,status):
   if request.user.is_authenticated and request.user.Role == 1: 
      return redirect('c_home',0) 
   if request.user.is_authenticated and request.user.Role == 2: 
      return redirect('v_home') 
   user=User.objects.get(id=user_id)
   email(user.id)
   if status != 'forgot':
     return redirect('verify_otp',user.id,'none')
   else:
     return redirect('verify_otp',user.id,'forgot')

#closed
# user logout
def logout(request):
   if request.user.Role == 1 or 2:
         authlogout(request)
         return redirect('index')
   elif request.is_admin:
      authlogout(request)
      return redirect('admin_log')
   else:
      return redirect('index')

# --------- closed dependencies funtions -------------->
