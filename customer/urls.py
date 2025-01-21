from django.urls import path
from . import views

app_name = 'customer'
urlpatterns = [
    path ('customerprofile/',views.customerProfile,name='customerProfile'),
    path ('address/<int:customer_id>/',views.address,name='address'),
    path ('user_auth/<int:user_id>/',views.user_auth,name='user_auth'),
    path ('change_password/<int:user_id>/',views.change_password,name='change_password'),
    path ('delete_address/<int:customer_id>/<int:address_id>/',views.delete_address,name='delete_address'),
    path ('update_address/<int:address_id>/',views.update_address,name='update_address'),
    path ('shop/<int:wishlist>/',views.shop,name='shop'),
    path ('single_product/<int:product_id>/<int:wishlist>/',views.single_product,name='single_product'),
    path ('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path ('view_cart/<int:product_id>/<int:wishlist>',views.view_cart,name='view_cart'),
    path('update-quantity/',views.update_quantity_in_cart, name='update_quantity'),
    path ('all_products_checkout',views.all_products_checkout,name='all_products_checkout'),
    path ('single_product_checkout/<int:cart_id>/',views.single_product_checkout,name='single_product_checkout'),
    path ('checkout_address/<int:address_id>/<str:status>/<int:cart_id>/',views.checkout_address,name='checkout_address'),
    path ('place_order/<int:cart_id>/<str:status>/',views.place_order,name='place_order'),
    path('order_history/',views.order_history, name='order_history'),
    path ('order_cancel/<int:order_id>/',views.order_cancel,name='order_cancel'),
    path ('search_product/',views.search_product,name='search_product'),
    path ('rasorpay/<int:order_id>/<str:status>/',views.rasorpay,name='rasorpay'),
    path('verify_payment/<int:order_id>/', views.verify_payment, name='verify_payment'),
    path('rasorpay_order_status/<int:order_id>/', views.rasorpay_order_status, name='rasorpay_order_status'),
    path('wallet/',views.My_wallet,name='wallet'),
    path('return_product/<int:order_id>/', views.return_product, name='return'),
    path('wishlist/<int:product>/',views.wishlist,name='wishlist'),
    path('invoice/<int:order_id>/',views.invoice_pdf_view,name='invoice'),

]
    
    
