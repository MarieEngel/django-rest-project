from django.contrib import admin
from django.urls import path

from .views import index, detail, delete_post, edit_post


urlpatterns = [
    path("", index, name="index"), 
    path("<id>/", detail, name="detail"),
    path("<id>/delete/", delete_post, name="delete_post"),
    path("<id>/edit/", edit_post, name="edit_post"),
    ]
