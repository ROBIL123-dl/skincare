from django.urls import path
from . import views

urlpatterns = [
   path('',views.index,name='index'),
   #customer side
   path('signup',views.Customer_sign_up,name='signup'),
   path('Customer_login/',views.Customer_login,name='c_login' ),
   path('customer_home/',views. Customer_home_page,name='c_home' ),
   
   #vendeor side
    path('vendor_login/',views.Vendor_login,name='v_login' ),
    path('v_signup',views.Vender_sign_up,name='v_signup'),
    path('vendor_home/',views. Vendor_home_page,name='v_home' ),
   
   #admin side
   path('admin_log/',views.Admin_login,name='admin_log' ),
   path('admin_home/',views.Admin_home_page,name='admin_home' ),
   path('customer_side/', views.Customer_side,name='customer_side' ),
   path('vendor_side/', views.Vendor_side,name='vendor_side' ),
   path('Block_customer/<int:user_id>/',views.Block_customer,name='Block_customer'),
   path('UnBlock_customer/<int:user_id>/',views.UnBlock_customer,name='UnBlock_customer'),
   path('Block_vendor/<int:user_id>/',views.Block_vendor,name='Block_vendor'),
   path('UnBlock_vendor/<int:user_id>/',views.UnBlock_vendor,name='UnBlock_vendor'),
   path('vender_approval/<int:user_id>/',views.vender_approval,name='vender_approval'),
   path('vender_approved/<int:user_id>/',views.vender_approved,name='vender_approved'),
   path('novender_approved/<int:user_id>/',views.novender_approved,name='novender_approved'),
   path('category/', views.category, name='category' ),
   path('del_category/<int:cat_id>/',views.delete_category,name='del_category'),
   path('update_category/<int:cat_id>/',views.update_category,name='update_category'),

   # dependencies
   path('verify_otp/<int:user_id>/',views.otp_verify,name='verify_otp'),
   path('reset_otp/<int:user_id>/',views.reset_otp,name='reset_otp'),
   path('logout/',views.logout,name='logout' ),
   # path('forgot_password/',views.forgot_password,name='forgot' ),
   
  
]
  
  
  
  

   
   
   
   
 
   








