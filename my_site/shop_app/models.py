from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return 'products/product_{pk}/preview/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):


    class Meta:
        ordering = ['name', 'price']
        verbose_name = _("product")
        verbose_name_plural = _("products")


    name = models.CharField(max_length=50, verbose_name='Название продукта', db_index=True)
    description = models.TextField(null=False, blank=True, verbose_name='Описание продукта', db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Цена', db_index=True)
    discount = models.PositiveSmallIntegerField(default=0, verbose_name='Скидка', db_index=True)
    created_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    archived = models.BooleanField(default=False, verbose_name='Архивировано', db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Создатель', db_index=True)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    def get_absolute_url(self):
        return reverse('shop_app:products_details', args=[str(self.pk)])




    def __str__(self) -> str:
        return f'Продукт ({self.name!r})'


def product_images_directory_path(instance: 'ProductImage', filename: str) -> str:
    return 'products/product_{pk}/images/{filename}'.format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_directory_path)
    discription_image = models.CharField(max_length=150, null=False, blank=True, verbose_name='Описание к картинке')




class Order(models.Model):

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    delivery_address = models.TextField(null=False, blank=True, verbose_name='Адрес доставки')
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name='Промокод')
    created_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Заказчик')
    products = models.ManyToManyField(Product, related_name='orders', verbose_name='Продукты')
    receipt = models.FileField(null=True, upload_to='order/receipts/', verbose_name='Чек')

    def get_absolute_url(self):
        return reverse('shop_app:order_detail', args=[str(self.pk)])
