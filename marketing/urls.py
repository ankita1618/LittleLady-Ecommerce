from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls import include, url
from django.conf.urls.static import static
from marketing import views

urlpatterns = [
                path('ajax/dismiss_marketing_msg/', views.dismiss_marketing_msg, name='dismiss_marketing_msg'),
                path('ajax/email_Signup/', views.email_signup, name='ajax_email_signup'),

]

