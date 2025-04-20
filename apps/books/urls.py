from django.urls import path
from  . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('browser/', views.browser, name='browser'),
    path('map/', views.map, name='map'),
]
