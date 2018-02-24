from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.equipment, name="equipment"),
    path('<slug>/', views.equipment_item, name="equipment_item"),
    path('checkout/', views.equipment_checkout, name="equipment_checkout"),
]
