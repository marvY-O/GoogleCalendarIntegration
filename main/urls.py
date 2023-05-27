from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('init/', views.GoogleCalendarInitView),
    path('redirect/', views.GoogleCalendarRedirectView),
]
