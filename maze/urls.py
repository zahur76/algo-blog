from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.maze, name="maze"),
    path("compute_maze", views.compute_maze, name="maze"),
]
