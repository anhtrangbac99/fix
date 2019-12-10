from django.urls import path

from . import views
from ass2 import settings
from django.templatetags.static import static

app_name = 'amazon'

urlpatterns = [
    path('',views.homepage,name = 'homepage'),
    path('register/',views.register,name = 'register'),
    path('login/', views.login,name='login'),
    path('sell/',views.sell,name='sell'),
    path('regiser_seller/',views.register_seller,name='register_seller'),
    path('cart/',views.cart,name='cart'),
    path('cart/checkout_shipment/',views.checkout_shipment,name='checkout_shipment'),
    path('cart/checkout_shipment/checkout_payment/',views.checkout_payment,name='checkout_payment'),
    path('single-product/',views.single_product,name='single_product'),
    path('category/',views.category,name='category'),
    path('sell-product/',views.sell_product,name='sell_product'),
    path('confirmation/',views.confirmation,name='confirmation'),
]
