from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.equipment_list, name="equipment_list"),
    path('checkout/', views.checkout_page, name="checkout_page"),
    path('checkout/validate-selection/', views.check_user_can_check_out_equipment, name="validate_equipment_selection"),
    path('checkout/check-out-items/', views.handle_equipment_checkout_form, name='check_out_items'),
    path('<slug>/', views.equipment_details, name="equipment_details"),
    path('category/<slug>/', views.equipment_category, name="equipment_category"),
    path('checkout/cancel/<checkout_id>/', views.cancel_checkout, name="cancel_checkout"),
    path('checkouts/<item_id>/', views.item_checkouts, name="item_checkouts"),
    path('admin-calendar/', views.admin_calendar, name="admin_calendar"),
    path('admin-calendar/events/', views.admin_events, name="admin_events"),
    path('admin-user-projects/', views.get_user_projects_json, name="admin_user_projects"),
]
