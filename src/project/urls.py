from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.projects, name="user_projects"),
    path('<int:id>/', views.project, name="project")
]
