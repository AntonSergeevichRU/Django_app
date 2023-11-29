from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shop_app.models import Order


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write('Создаю заказ')
        user = User.objects.get(username='Admin')
        order = Order.objects.get_or_create(
            delivery_address='СССР ул.Ленина дом 5',
            promocode='PUTIN123',
            user=user,
        )
        self.stdout.write(f'Создан заказ {order}')