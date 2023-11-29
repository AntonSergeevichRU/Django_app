from django.contrib.sitemaps import Sitemap
from .models import Product


class ShopSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Product.objects.order_by('-created_in')

    def lastmod(self, obj: Product):
        return obj.created_in
