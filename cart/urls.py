from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls import include, url
from django.conf.urls.static import static
from cart import views

urlpatterns = [
                path('cart/', views.view, name='cart'),
                path('cart/<id>/', views.add_to_cart, name='add_to_cart'),
                path('cart/<id>/<slug:slug>', views.remove_from_cart, name='remove_from_cart'),

]

