from django.contrib import admin
from django.urls import path

from .views import index, detail, delete_post, edit_post, add_post


urlpatterns = [
    path("", index, name="index"), 
    path("add/", add_post, name="add_post"),
    path("<id>/", detail, name="detail"),
    path("<id>/delete/", delete_post, name="delete_post"),
    path("<id>/edit/", edit_post, name="edit_post"),
   
    ]
