"""faypublic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),

    # authentication
    path('register/', views.user_register, name="user_register"),
    path('login/', auth_views.login, {
        'template_name': 'user_login.html'
    }, name="user_login"),
    path('logout/', auth_views.logout, {
        'next_page': '/login/'
    }, name="user_logout"),
    path('reset-password/', auth_views.password_reset, {
        'template_name': 'user_password_reset.html'
    }, name="password_reset"),
    path('reset-password/done/',  auth_views.password_reset_done, {
        'template_name': 'user_password_reset_done.html'
    }, name="password_reset_done"),
    path('reset-password/<uidb64>/<token>/', auth_views.password_reset_confirm, {
        'template_name': 'user_password_reset_confirm.html'
    }, name="password_reset_confirm"),
    path('reset-password/complete/', auth_views.password_reset_complete, {
        'template_name': 'user_password_reset_complete.html'
    }, name="password_reset_complete"),

    # profile
    path('profile/', include('userprofile.urls')),

    # class
    path('classes/', include('classes.urls')),
    path('equipment/', include('inventory.urls')),
    # path('test-notifications/', views.test_notifications, name="test_notifications"),
    path('report/', include('report.urls'))
]
