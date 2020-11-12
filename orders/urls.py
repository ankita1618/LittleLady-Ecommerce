from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls import include, url
from django.conf.urls.static import static
from orders import views

urlpatterns = [
                path('checkout/', views.checkout, name='checkout'),
                path('orders/', views.orders, name='user_orders'),

]

