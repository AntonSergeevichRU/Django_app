
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'blog'

urlpatterns = [
    path('', BasedView.as_view(), name='blog'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('articles/latest/feed/', LatestArticlesFeed(), name='article_latest_feed'),
]