from django.urls import path
from .views import *


app_name ='my_api_app'
urlpatterns = [
    path('hello/', hello_api_view, name='hello_api'),
    path('groups/', GroupListView.as_view(), name='groups_api'),
]