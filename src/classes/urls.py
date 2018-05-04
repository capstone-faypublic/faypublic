from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.class_list, name="class_list"),
    path('<slug>/', views.class_registration, name="class_registration")
]
