from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.equipment_list, name="equipment_list"),
    path('checkout/<slug>/', views.equipment_checkout, name="equipment_checkout"),
    path('category/<slug>/', views.equipment_category, name="equipment_category"),
    path('checkout/cancel/<checkout_id>/', views.cancel_checkout, name="cancel_checkout"),
    path('checkouts/<item_id>/', views.item_checkouts, name="item_checkouts"),
    path('admin-calendar/', views.admin_calendar, name="admin_calendar"),
    path('admin-calendar/events/', views.admin_events, name="admin_events")
]
