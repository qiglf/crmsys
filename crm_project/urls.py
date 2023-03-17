from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('home/contacts/details/<int:id>', views.details, name='details'),
    path('home/search/details/<int:id>', views.details, name='details'),
    path('home/contacts/details/<int:id>/edit/', views.edit_details, name='edit_details'),
    path('home/contacts/details/<int:id>/delete/', views.delete_member, name='delete_member'),
    path('home/contacts/add/', views.add_member, name='add_member'),
    # home

    path("main/", views.main, name='main'),

    # contacts
    path("home/contacts/", views.contacts, name='contacts'),
    path('home/search/', views.contactSearch, name='contact_search'),

    path("admin/", admin.site.urls),

    path("accounts/", include("django.contrib.auth.urls")),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),


]