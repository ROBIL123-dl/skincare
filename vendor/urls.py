from django.urls import path,include
from . import views
app_name = 'vendor'
urlpatterns = [
    path('vendorprofile',views.vendor_profile,name='vendorprofile'),
    path ('vendor_auth/<int:user_id>/',views.user_auth,name='vendor_auth'),
    path ('change_password/<int:user_id>/',views.change_password,name='change_password'),
    path('subcategory',views.add_subcategory,name='subcategory'),
    path('create_product',views.create_product,name='create_product'),
    path('product_list',views.product_list,name='product_list'),
    path ('product_update/<int:product_id>/',views.product_update,name='product_update'),
    path ('block_product/<int:product_id>/<str:status>/',views.block_product,name='block_product'),
    path('order_list/',views.order_list,name='order_list'),
    path('order_detail/<int:order_id>/',views.order_details,name='order_detail'),
    path('sales_report/',views.sales_report,name='sales_report'),
    path ('pdf_download/<str:period>/<str:type>/',views.generate_pdf_view,name='pdf_download'),
    path ('excel_download/<str:period>/<str:type>/',views.html_to_excel_view,name='excel_download'),

]
