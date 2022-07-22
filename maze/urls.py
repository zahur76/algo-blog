from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.maze, name="maze"),
    path("compute_maze", views.compute_maze, name="compute_maze"),
    path("reset_maze", views.reset_maze, name="reset_maze"),
]
