from django.urls import path
from django.contrib.auth import views as auth_views
from . import dashboard_views, views

urlpatterns = [
    path("admin/", dashboard_views.dashboard_login, name="dashboard_login"),
    path(
        "dashboard/logout/", dashboard_views.dashboard_logout, name="dashboard_logout"
    ),
    path("dashboard/", dashboard_views.dashboard_home, name="dashboard_home"),
    path(
        "dashboard/content/<slug:key>/",
        dashboard_views.singleton_edit,
        name="dashboard_singleton_edit",
    ),
    path(
        "dashboard/<slug:key>/add/",
        dashboard_views.collection_create,
        name="dashboard_collection_create",
    ),
    path(
        "dashboard/<slug:key>/<int:pk>/edit/",
        dashboard_views.collection_edit,
        name="dashboard_collection_edit",
    ),
    path(
        "dashboard/<slug:key>/<int:pk>/delete/",
        dashboard_views.collection_delete,
        name="dashboard_collection_delete",
    ),
    path(
        "dashboard/<slug:key>/",
        dashboard_views.collection_list,
        name="dashboard_collection_list",
    ),
    # Password Reset URLs
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="dashboard/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="dashboard/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="dashboard/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="dashboard/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("about/", views.about, name="about"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("contact/", views.contact, name="contact"),
    path("testimonials/submit/", views.submit_testimonial, name="submit_testimonial"),
]
