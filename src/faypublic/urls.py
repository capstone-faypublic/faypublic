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
    path('', views.home),
    path('admin/', admin.site.urls),

    # authentication
    path('register/', views.user_register, name="user_register"),
    path('login/', auth_views.login, {
        'template_name': 'user_login.html'
    }, name="user_login"),
    path('logout/', auth_views.logout, {
        'next_page': '/'
    }, name="user_logout"),

    # profile
    path('profile/', include('userprofile.urls')),

    # equipment checkout
    path('checkout/', include('equipmentcheckout.urls')),

    # course
    path('courses/', include('courses.urls')),
]
