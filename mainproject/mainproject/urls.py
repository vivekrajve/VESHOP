"""mainproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appsone import views

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index,name="index"),
    path('login',views.login,name='login'),
    path('contact',views.contact,name='contact'),
    path('adminindex', views.adminindex, name='adminindex'),
    path('orders', views.orders, name='orders'),
    path('user_details', views.user_details, name='user_details'),
    path('employee_details', views.employee_details, name='employee_details'),
    path('Add_product', views.Add_product, name='Add_product'),
    path('Manage_Product', views.Manage_Product, name='Manage_Product'),
    path('admin_profile', views.admin_profile, name='admin_profile'),
    path('messages', views.message, name='messages'),
    path('user_register', views.user_reg, name='user_register'),
    path('employee_register', views.employee_register, name='employee_register'),
    path('employee_register_2', views.employee_register_2, name='employee_register_2'),
    path('userindex', views.userindex, name='userindex'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('delivery_boy_profile', views.delivery_boy_profile, name='delivery_boy_profile'),
    path('delivery_index', views.delivery_index, name='delivery_index'),
    path('delivery_orders', views.delivery_orders, name='delivery_orders'),
    path('employee_profile', views.employee_profile, name='employee_profile'),
    path('category', views.category, name='category'),
    path('user_category', views.user_category, name='user_category'),

    path('cart', views.cart, name='cart'),
    path('single_product/<int:d>', views.single_product, name='single_product'),
    path('confirmation/<int:d>', views.confirmation, name='confirmation'),
    path('user_edit', views.user_edit, name='user_edit'),
    path('edit_product/<int:d>', views.edit_product, name="edit_product"),
    path('delete/<int:d>', views.delete),
    path('update_product', views.update_product, name='update_product'),
    path('Approve/<int:d>', views.Approve, name="Approve"),
    path('Reject/<int:d>', views.Reject, name="Reject"),
    path('edit_user', views.edit_user, name='edit_user'),
    path('add_wishlist/<int:d>', views.add_wishlist, name="add_wishlist"),
    path('user_wish', views.user_wish, name='user_wish'),
    path('remove_wishlist/<int:d>', views.remove_wishlist, name='remove_wishlist'),
    path('add_cart/<int:d>', views.add_cart, name='add_cart'),
    path('remove_cart/<int:d>', views.remove_cart, name='remove_cart'),
    path('increment/<int:d>', views.increment, name='increment'),
    path('decrement/<int:d>', views.decrement, name='decrement'),
    path('confirmation_cart', views.confirmation_cart, name='confirmation_cart'),
    path('payment/<int:data1>', views.payment, name='payment'),
    path('payment2/<int:data1>', views.payment2, name='payment2'),
    path('search_page', views.search_page, name='search_page'),
    path('product_list_view', views.product_list_view, name='product_list_view'),
    path('admin_login', views.admin_login, name='admin_login'),

    path('admin_edit', views.admin_edit, name='admin_edit'),
    path('edit_admin', views.edit_admin, name='edit_admin'),
    path('employee_edit', views.employee_edit, name='employee_edit'),
    path('edit_employee', views.edit_employee, name='edit_employee'),
    path('user_order', views.user_order, name='user_order'),
    path('paid_cart', views.paid_cart, name='paid_cart'),
    path('paid_single_product', views.paid_single_product, name='paid_single_product'),
    path('dispatch/<int:id>', views.dispatch_order, name='dispatch_order'),
    path('dispatch_order_delivered/<int:id>', views.dispatch_order_delivered, name='dispatch_order_delivered'),
    path('contact_add', views.contact_add, name='contact_add'),
    path('Ads', views.Ads, name='Ads'),
    path('Manage_Ads', views.Manage_Ads, name='Manage_Ads'),
    path('delete_ads/<int:d>', views.delete_ads),



]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)