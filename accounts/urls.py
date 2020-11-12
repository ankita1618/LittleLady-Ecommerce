from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls import include, url
from django.conf.urls.static import static
from accounts import views

urlpatterns = [
                path('logout/', views.logout_view, name='auth_logout'),
                path('login/', views.login_view, name='auth_login'),
                path('accounts/register/', views.registration_view, name='auth_register'),
                path('activate/<str:activation_key>/', views.activation_view, name='activation_view'),

]

#062ce3a60074225569c64d38225e6bd7337d8b88