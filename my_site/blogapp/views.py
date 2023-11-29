from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from .models import *

class BasedView(ListView):
    template_name = 'blogapp/basa.html'
    queryset = (
        Article.objects.
            select_related('author', 'category').
            prefetch_related('tags').
            defer('content', 'author__bio')

    )




class ArticleListView(ListView):

    queryset = (
        Article.objects.order_by('-pub_date')
    )


class ArticleDetailView(DetailView):
    model = Article



class LatestArticlesFeed(Feed):
    title = 'Blog articles (latest)'
    description = 'Updates on changes and addition blog articles'
    link = reverse_lazy('blog:articles')

    def items(self):
        return (
        Article.objects.order_by('-pub_date')[:3]
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]

    def item_link(self, item):
        return reverse('blog:article', kwargs={'pk': item.pk})