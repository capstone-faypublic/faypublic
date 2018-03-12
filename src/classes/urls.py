from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.class_list, name="class_list"),

]




# from django.urls import path, include
# from . import views
# from django.contrib.auth import views as auth_views
#
# urlpatterns = [
#     path('', views.user_profile, name="user_profile"),
#     # user projects in production
#     path('projects/', include('project.urls'))
# ]
