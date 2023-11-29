# Generated by Django 4.2.2 on 2023-07-31 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название продукта')),
                ('description', models.TextField(blank=True, verbose_name='Описание продукта')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Цена')),
                ('discount', models.PositiveSmallIntegerField(default=0, verbose_name='Скидка')),
                ('created_in', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('archived', models.BooleanField(default=False, verbose_name='Архивировано')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'ordering': ['name', 'price'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_address', models.TextField(blank=True, verbose_name='Адрес доставки')),
                ('promocode', models.CharField(blank=True, max_length=20, verbose_name='Промокод')),
                ('created_in', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('products', models.ManyToManyField(related_name='orders', to='shop_app.product', verbose_name='Продукты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
            ],
        ),
    ]