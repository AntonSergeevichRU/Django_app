from string import ascii_letters
from random import choices

from django.contrib.auth.models import Permission, User


from django.test import TestCase
from django.urls import reverse, reverse_lazy

from .models import *
from .utils import add_numbers
from django.conf import settings


class AddNumbersTestCase(TestCase):
    def test_add_numbers(self):
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='john', password='johnpassword')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


    def setUp(self) -> None:
        self.name = ''.join(choices(ascii_letters, k=10))
        self.client.force_login(self.user)
        permission = Permission.objects.get(codename='add_product')
        self.user.user_permissions.add(permission)


    def test_product_create(self):
        response = self.client.post(
            reverse('shop_app:create_product'),
            {
                'name': self.name,
                'price': "123.45",
                'description': "A good table",
                'discount': "10",
            }
        )
        print(f'ответ-> {response}')
        self.assertRedirects(response, reverse('shop_app:products_list'))
        self.assertTrue(Product.objects.filter(name=self.name).exists())


class ProductDetailsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='john', password='johnpassword')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.product_name = ''.join(choices(ascii_letters, k=7))
        self.product = Product.objects.create(name=self.product_name, created_by=self.user)

    def tearDown(self) -> None:
        self.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shop_app:products_details', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shop_app:products_details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'user-fixtures.json',
        'products-fixtures.json',
    ]

    def test_products(self):

        #1
        # response = self.client.get(reverse('shop_app:products_list'))
        # for product in Product.objects.filter(archived=False).all():
        #     self.assertContains(response, product.name)

        #2
        #self.assertTemplateUsed(response, "shop_app/products_list.html")
        # response = self.client.get(reverse('shop_app:products_list'))
        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context['Products']
        #
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)

        #3
        # response = self.client.get(reverse('shop_app:products_list'))
        # for product in Product.objects.filter(archived=False).all():
        #      self.assertContains(response, product.name)

        #4
        response = self.client.get(reverse('shop_app:products_list'))
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['Products']),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, "shop_app/products_list.html")



class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='john', password='johnpassword')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


    def setUp(self):
        self.client.force_login(self.user)

        self.order = Order.objects.create(
            delivery_address='Куда то доставить',
            promocode='putin',
            user=self.user
        )

    def tearDown(self):
        self.order.delete()


    def test_order_details(self):
        response = self.client.get(reverse('shop_app:order_detail', kwargs={'pk': self.order.pk}))
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context['order'].pk, self.order.pk)



class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='john', password='johnpassword')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse('shop_app:order_list'))
        self.assertContains(response, 'Order')

    # def test_orders_view_not_authenticated(self):
    #     self.client.logout()
    #     response = self.client.get(reverse('shop_app:order_list'))
    #     #self.assertRedirects(response, str(settings.LOGIN_URL))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertIn(str(settings.LOGIN_URL),response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'user-fixtures.json',
        'products-fixtures.json',
    ]


    def test_get_products_view(self):
        response = self.client.get(reverse('shop_app:products_export'))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        print(f'ПРОДУКТЫ {products}')
        expected_data = [
            {'pk': product.pk,
             'name': product.name,
             'price': str(product.price),
             'archived': product.archived,
             }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data,
        )



class OrderExportTestCase(TestCase):

    fixtures = [
        'user-fixtures.json',
        'products-fixtures.json',
        'orders-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        super(OrderExportTestCase, cls).setUpClass()
        cls.user = User.objects.create_user(username='TestUser', password='TestUserpassword', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super(OrderExportTestCase, cls).tearDownClass()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(reverse('shop_app:orders_export'))

        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()

        expected_data = [
            {
                'pk': order.pk,
                'promocode': order.promocode,
                'delivery_address': order.delivery_address,
                'products':[{
                 'name': product.name,
                }
                for product in order.products.all()
                ]
            }
            for order in orders
        ]
        orders_data = response.json()

        self.assertEqual(
            orders_data['orders'],
            expected_data,
        )
