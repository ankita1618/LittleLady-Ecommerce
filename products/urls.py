from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls import include, url
from django.conf.urls.static import static
from products import views

urlpatterns = [
                  path('', views.home, name='home_new'),
                  path('products/', views.all, name='all_products'),  # URL for all
                  path('products/<slug:slug>/', views.single, name='single_products'),
                  # (?P<slug>[\w-]+) in EDIT2020 <slug:slug> /// <int:slug>
                  # url for single product and() will take the the argument passed in the 'single' funcn in views.py
                  path('s/', views.search, name='search'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    #     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
