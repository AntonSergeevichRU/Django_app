from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'map'

urlpatterns = [
    path('', info),
  ]