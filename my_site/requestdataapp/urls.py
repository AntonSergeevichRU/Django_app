
from django.urls import path
from .views import *

app_name ='requestdataapp'

urlpatterns = [
    path('get/', process_get_view, name='req'),
    path('bio/', user_form, name='user_form'),
    path('upload/', handle_file_upload, name='upload'),
    ]