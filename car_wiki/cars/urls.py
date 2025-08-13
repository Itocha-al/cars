# cars/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.brand_list, name='brand_list'),
    path('brand/<int:brand_id>/', views.model_list, name='model_list'),
    path('model/<int:model_id>/', views.model_detail, name='model_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
