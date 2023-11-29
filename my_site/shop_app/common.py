from csv import DictReader
from io import TextIOWrapper

from .models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)
    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)

    orders = [row for row in reader]
    order_list = []
    products_list = []

    print(orders)

    for order in orders:
        order_list.append(Order(
            delivery_address=order['delivery_address'],
            promocode=order['promocode'],
            user_id=order['user_id'],

        ))

        products_list.append([int(product) for product in order['products'] for em in product if em.isdigit()])

    Order.objects.bulk_create(order_list)

    for elem in range(len(products_list)):
        prod = Product.objects.filter(id__in=products_list[elem])

        order_list[elem].products.set(prod)

    return order_list
