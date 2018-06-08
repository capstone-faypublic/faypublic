from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.projects, name="user_projects"),
    path('<int:id>/', views.project, name="project"),
    path('cancel/<int:project_id', views.cancel_project, name='cancel_project')
]
