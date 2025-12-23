from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "backOffice"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("agencies/", views.manage_agencies, name="manage_agencies"),
    path("agencies/<int:agency_id>/", views.agency_detail, name="agency_detail"),
    path("agencies/approve/<int:agency_id>/", views.approve_agency, name="approve_agency"),
    path("agencies/reject/<int:agency_id>/", views.reject_agency, name="reject_agency"),
    path("subscriptions/", views.manage_subscriptions, name="manage_subscriptions"),
    path("users/", views.users_list, name="users_list"),
    path("subscriptions/edit/<int:sub_id>/", views.edit_subscription, name="edit_subscription"),
    path("subscriptions/renew/<int:sub_id>/", views.renew_subscription, name="renew_subscription"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/admin/login/"), name="logout"),
]
