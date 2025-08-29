from django.urls import path
from . import views

urlpatterns = [
    path('', views.BrandListView.as_view(), name='brand_list'),
    path('brand/<int:brand_id>/', views.ModelListView.as_view(), name='model_list'),
    path('model/<int:model_id>/', views.CarModelDetailView.as_view(), name='model_detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
