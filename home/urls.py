from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("/send_comment", views.send_comment, name="send_comment"),
]
