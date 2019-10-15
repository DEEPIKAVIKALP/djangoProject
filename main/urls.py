"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path
from django.conf.urls import url
from . import views

app_name = "main"

urlpatterns = [
    path("",views.homepage, name = "homepage"),
    path("index.html",views.homepage, name = "homepage"),
    #path("products/",views.products, name = "products"),
    path("shop/",views.shop, name = "products"),
    path("cart/",views.cart, name = "cart"),
    path("cart/<int:cart_id>/",views.cart_item_remove, name = "cart_item_remove"),
    path("cart/<int:cart_id>/<int:quantity>",views.update_cart_quantity, name = "update_cart_quantity"),
    url(r'^shop/(?P<product_id>[0-9]+)/$', views.item_details, name = 'item_details'),
    #need to remove next line
    #url(r'^products/(?P<slug>pottery)/(?P<product_id>[0-9]+)/$', views.item_details, name = 'item_details'),
    
    #url(r'^products/<text:text>/(?P<product_id>[0-9]+)/$', views.item_details, name = 'item_details'),
    path('shop/<str:slug>/', views.product_category,name = "product_category" ),
    #url(r'^products/(\d+)/', views.product_details, name = 'product_details'),
    
    path("register.html/", views.register, name="register"),
    path("login/",views.login_requested, name='login'),
    path("login/register/", views.register, name="register"),
    path("logout/",views.logout_requested, name='logout'), 
    path("checkout/",views.checkout, name='checkout'), 
    path("placeorder/<int:address_id>",views.placeorder, name='placeorder'), 

    path("shop/<int:product_id>/<int:quantity>/", views.Add_To_Cart, name = 'Add_To_Cart'),
    path("thankyou/<int:address_id>/<str:payment_mode>",views.thankyou, name='thankyou'), 
    path("order_history/", views.order_history, name="order_history"),
    path("profile/",views.profile, name = "profile"),
    path("change_profile/",views.change_profile, name = "change_profile"),
    path("change_password/",views.change_password, name = "change_password"),
    path("forgot_password/",views.forgot_password, name="forgot_password"),
    path("cancel_order/<int:order_detail_id>",views.cancelorder, name='cancelorder')
]
