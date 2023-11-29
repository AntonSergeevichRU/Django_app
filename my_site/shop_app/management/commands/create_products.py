from django.core.management import BaseCommand

from shop_app.models import Product


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write('Создаю продукты в таблицу')
        products_name = [
            'Ahmad Tea',
            'Greenfield',
            'Brizton',
            'AZERCAY',
            'NikTea',
        ]
        for tea in products_name:
            product, created = Product.objects.get_or_create(name=tea)
            self.stdout.write(f'Создан продукт {tea}')

        self.stdout.write(self.style.SUCCESS('Продукты созданы'))