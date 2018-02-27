from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.equipment_list, name="equipment_list"),
    path('checkout/<slug>/', views.equipment_checkout, name="equipment_checkout"),
    path('category/<slug>/', views.equipment_category, name="equipment_category") 
]
