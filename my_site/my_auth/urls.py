from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *

app_name ='my_auth'

urlpatterns = [

    path('login/', LoginView.as_view(
        template_name='my_auth/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),

    path('about/', AboutMyView.as_view(), name='about'),
    path('about/<int:pk>/', DetailUserView.as_view(), name='user_detail'),
    path('about/<int:pk>/update/', UpdateProfile.as_view(), name='user_update'),
    path('about/list/', UserListView.as_view(), name='user_list'),
    path('register/', RegisterUserView.as_view(), name='register'),

    path('cookie/get/', get_cookie_view, name='cookie_get'),
    path('cookie/set/', set_cookie_view, name='cookie_set'),
    path('session/get/', get_session_view, name='session_get'),
    path('session/set/', set_session_view, name='session_set'),

    path('foo-bar/', FooBarView.as_view(), name='foo_bar'),

    path('hello/', HelloView.as_view(), name='hello'),

    ]