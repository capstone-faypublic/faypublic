from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_profile, name="user_profile"),
    path('edit/', views.edit_profile, name='edit_profile'),
    # user projects in production
    path('projects/', include('project.urls')),
    path('checkouts/', views.user_checkouts, name="user_checkouts"),
    path('classes/', views.user_classes, name="user_classes")
]
