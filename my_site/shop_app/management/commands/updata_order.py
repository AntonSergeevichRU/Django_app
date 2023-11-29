from django.core.management import BaseCommand
from shop_app.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        order = Order.objects.first()
        if not order:
            self.stdout.write('Нет заказов')
            return
        products = Product.objects.all()
        for product in products:
            order.products.add(product)
        order.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully and products {order.products.all()} to order {order}'
            )
        )