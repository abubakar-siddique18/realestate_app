# listings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
     path('login/', views.login_page, name='user_login'),
    path('logout/', views.logout, name='logout'),
    path('property/create/', views.property_create, name='property_create'),
    path('property/update/<int:pk>/', views.property_update, name='property_update'),
    path('property/delete/<int:pk>/', views.property_delete, name='property_delete'),
    path('my_properties/', views.my_properties, name='my_properties'),
    path('', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('like-property/<int:pk>/', views.like_property, name='like_property'),
]
