from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('browser/', views.browser, name='browser'),
    path('map/', views.map, name='map'),
    path('shelf/saved/', views.shelf_saved, name='shelf_saved'),
    path('shelf/borrowed/', views.shelf_borrowed, name='shelf_borrowed'),
    path('shelf/purchased/', views.shelf_purchased, name='shelf_purchased'),
]
