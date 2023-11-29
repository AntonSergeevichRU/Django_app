from django.contrib.auth.decorators import permission_required, login_required

import logging
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404, reverse
from timeit import default_timer
from django.urls import reverse_lazy

from csv import DictWriter

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView

from .common import save_csv_products
from .forms import *
from .models import *

from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action

from django.core.cache import cache

log = logging.getLogger(__name__)


@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('pk')
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,

        OrderingFilter,
    ]
    search_fields = [
        'name',
        'description',
    ]

    ordering_fields = [
        'pk',
        'price',
        'name',
    ]

    @extend_schema(
        summary='GET one product by ID',
        description='Retrieves product? returns 404 is not found',
        responses={
            200: ProductSerializer,
            400: OpenApiResponse(description='Empty response, product by id not found')
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'product-export.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response

    @action(
        detail=False,
        methods=['post'],
        parser_classes=[MultiPartParser],
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by('pk')
    serializer_class = OrderSerializer
    filter_backends = [

        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        'user',
        'delivery_address',
        'promocode',
        'products',
    ]

    ordering_fields = [
        'pk',
        'created_in',
    ]




class ShopInfo(View):
    def get(self, request):
        products = Product.objects.all()
        context = {
            'items': 1,
        }
        log.debug('Products for shop index: %s', products)
        log.info('Rendering shop index')
        return render(request, 'shop_app/shopping.html', context=context)


# Класс просмотра списка продуктов
class ProductListView(ListView):
    template_name = 'shop_app/products_list.html'
    #    model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'Products'


# Класс просмотра информации о продукте
class ProductDetails(DetailView):
    template_name = 'shop_app/product_details.html'
    # model = Product
    queryset = Product.objects.filter(archived=False).prefetch_related('images')
    context_object_name = 'Products'


# Класс создания продукта
class ProductCreate(PermissionRequiredMixin, CreateView):
    model = Product
    permission_required = 'shop_app.add_product'
    # form_class = AddProductForm
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shop_app:products_list')

    #
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# Класс обновления продукта
class ProductUpdate(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.request.user.is_superuser or \
               self.request.user.id == self.get_object().created_by.id


    model = Product
    #fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = '_update_form'
    form_class = AddProductForm

    def get_success_url(self):
        return reverse(
            'shop_app:products_details',
            kwargs={'pk': self.object.pk},
        )

    def form_valid(self, form):
        response = super(ProductUpdate, self).form_valid(form)

        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return response



class ProductDell(UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.id == self.get_object().created_by.id

    model = Product
    success_url = reverse_lazy('shop_app:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)



class LatestProductsFeed(Feed):
    title = 'Shop Products (latest)'
    description = 'Updates on changes and addition shop products'
    link = reverse_lazy('shop_app:articles')

    def items(self):
        return (
        Product.objects.order_by('-created_in')[:3]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


class CreateOrder(LoginRequiredMixin, CreateView):
    model = Order
    fields = 'user', 'delivery_address', 'products', 'promocode'
    success_url = reverse_lazy('shop_app:order_list')


class OrderList(LoginRequiredMixin, ListView):
    queryset = Order.objects.select_related('user').prefetch_related('products')
    context_object_name = 'Orders'


class OrderDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'shop_app.view_order'
    queryset = Order.objects.select_related('user').prefetch_related('products')


class OrderUpdate(UpdateView):
    model = Order
    fields = 'user', 'delivery_address', 'promocode', 'products'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse(
            'shop_app:order_detail',
            kwargs={'pk': self.object.pk},
        )


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('shop_app:order_list')


class ProductsDataExportView(View):
    def get(self, request):
        products = Product.objects.order_by('pk').all()
        products_data = [
            {'pk': product.pk,
             'name': product.name,
             'price': product.price,
             'archived': product.archived,
             }
            for product in products
        ]
        mame = Product.objects.all()
        print(mame)
        return JsonResponse({'products': products_data})


class OrderDataExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {'pk': order.pk,

             'promocode': order.promocode,
             'delivery_address': order.delivery_address,
             'products': [{
                 'name': product.name,
                }
                for product in order.products.all()
                ]
             }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})


class UserOrdersListView(ListView):

    template_name = 'shop_app/user_orders.html'
    context_object_name = 'user_orders'

    def get_queryset(self, **kwargs):
        self.owner = get_object_or_404(User, pk=self.kwargs['user_id'])
        return Order.objects.filter(user=self.owner).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class UserOrdersExportView(View):

    # def get_queryset(self, **kwargs):
    #
    #     return Order.objects.filter(user=self.owner)

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(User, pk=self.kwargs['user_id'])
        cache_key = 'user_orders_data_export_' + str(self.kwargs['user_id'])
        user_orders_data = cache.get(cache_key)
        if user_orders_data is None:
            orders = Order.objects.filter(user=owner).all().order_by('pk')
            print(orders)
            user_orders_data = OrderSerializer(orders, many=True)
            cache.set(cache_key, user_orders_data, 30)
        return JsonResponse({'user_orders': user_orders_data.data})
