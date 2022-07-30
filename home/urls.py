from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("part_two", views.part_two, name="part_two"),
    path("compute_paths", views.compute_paths, name="compute_paths"),
    path("send_comment", views.send_comment, name="send_comment"),
]
