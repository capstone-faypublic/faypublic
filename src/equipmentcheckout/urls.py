from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.equipment, name="equipment"),
    path('checkout/', views.equipment_checkout, name="equipment_checkout"),
]
