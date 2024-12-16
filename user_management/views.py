from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.cache import cache_control
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login,logout as authlogout
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import *
from .utils import *

def is_user(user):
    return user.is_authenticated == False
@user_passes_test(is_user)
def index(request):
    return render(request,'index.html')
  
  
# <--------admin side funtions---------->

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Admin_login(request):
  if request.user.is_authenticated and request.user.Role == 1:  
      return redirect('c_home')
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
    return render(request,'custom_admin/home.html')
# closed admin home 
# admin customer side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_log')
def Customer_side(request):
   customer=Customer_profile.objects.all()
   if customer == None:
      messages.error(request," No customers found !")
   else:
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
   vendor=Vendor_profile.objects.all()
   if vendor == None:
       messages.error(request," No vendors found !")
   else:
     context = {
      'vendor': vendor
       }
   return render(request,'custom_admin/vendor.html',context)
# closed
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
         vender_user.is_staff = True
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
      category.name=name
      category.desc=desc
      category.save()
      return redirect('category')
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
# <--------admin side funtions closed---------->

#<-------------------customer side funtions------------------->

# customer sign up
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Customer_sign_up(request):
  if request.user.is_authenticated and request.user.Role == 1:  
      return redirect('c_home')
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
            return redirect('verify_otp',user.id)
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
      return redirect('c_home')
   elif request.user.is_authenticated and request.user.Role == 2:
      return redirect('v_home')                                    
   elif request.user.is_authenticated and request.user.is_admin:
      return redirect('admin_home')
   if request.user.is_authenticated and request.user.Role == 1: 
      return redirect('c_home') 
   form = customerLogin()
   if request.method == 'POST':
      form = customerLogin(request.POST)
      if form.is_valid():
            email = form.cleaned_data.get('email_id')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
             if user.Role == 1 and user.is_active == True:
                login(request, user)
                return redirect('c_home')
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
def Customer_home_page(request):
   if request.user.is_authenticated and request.user.Role == 2: 
         return redirect('v_home') 
   return render(request,'customer/customer_home.html')
#closed
#<-------------------customer side funtions closed------------------->


#<-------------------vendor side funtions------------------->

#vendor sign-up
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Vender_sign_up(request):
  if request.user.is_authenticated and request.user.Role == 1:  
      return redirect('c_home')
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
            return redirect('verify_otp',user.id)
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
      return redirect('c_home')
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
            vendor=authenticate(email=email, password=password)
            if vendor is not None:
              if vendor.Role == 2 and vendor.is_active == True and vendor.is_staff == True:
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
    return render(request,'vendor/dashboard.html')
#closed

#<-------------------vendor side funtions closed------------------->

# ---------dependencies funtions -------------->
# verify otp
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otp_verify(request,user_id):
   if request.user.is_authenticated and request.user.Role == 1: 
      return redirect('c_home') 
   if request.user.is_authenticated and request.user.Role == 2: 
      return redirect('v_home') 
   user=get_object_or_404(User,id=user_id)
   if request.method == 'POST':
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
     if verify_otp(single_number_otp,user.otp): #funtion call for verify otp in utils.py
        user.otp=None
        user.save()
        if user.Role == 1:
           return redirect('c_login')
        elif user.Role == 2:
           return redirect('v_login')
     else:
        messages.error(request," Please Enter correct otp !")
   return render(request,'otp_verify.html',{'user':user})
#closed
# reset otp
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_otp(request,user_id):
   if request.user.is_authenticated and request.user.Role == 1: 
      return redirect('c_home') 
   if request.user.is_authenticated and request.user.Role == 2: 
      return redirect('v_home') 
   user=User.objects.get(id=user_id)
   email(user.id)
   return redirect('verify_otp',user_id=user.id)
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
# closed
# def forgot_password(request):
#    if request.method == 'POST':
#       email = request.POST.get('email')
#       user=get_object_or_404(User,email=email)
#       if user:
#        if email(id=user.id):
#            return redirect('verify_otp',user.id,'forgot')

# def change_for_password(request,user_id,value):
#    if request.method == 'POST':
#     if value == True:
#       password = request.POST.get('password')
#       c_password= request.POST.get('c_password')
#       user=get_object_or_404(User,id=user_id)
#       if password == c_password:
#             user.password=make_password(password)  
#             user.save()
#             if user.Role == 1:
#                  return redirect('c_login')
#             elif user.Role == 2:
#                  return redirect('v_login')
#       else:
#              messages.error(request," Both password are not same ")
#     else:
#         messages.error(request,"Enter correct OTP ")
      
#    return render(request,'change_password.html')
   
# --------- closed dependencies funtions -------------->
 


 


 








   


   

       








