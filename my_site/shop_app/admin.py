from csv import DictReader
from io import TextIOWrapper

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.shortcuts import render, redirect

from .common import save_csv_products, save_csv_orders
from .admin_mixins import ExportAsCSVMixin
from .forms import *


class OrderInline(admin.TabularInline):
    model = Product.orders.through



class ProductInline(admin.StackedInline):
    model = ProductImage


@admin.action(description='Архивировать продукт')
def mark_archived(modelAdmim: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Удалить из архива продукт')
def dell_archived(modelAdmim: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)





@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = 'shop_app/products_changelist.html'
    actions = [
        mark_archived,
        dell_archived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
        ProductInline,
    ]
    list_display = 'pk', 'name', 'description', 'price', 'discount', 'archived',
    list_display_links = 'pk', 'name',
    ordering = 'pk',
    search_fields = 'pk', 'name', 'price',
    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),

        ('Price options', {
            'fields': ('price', 'discount',),
            'classes': ('collapse', 'wide',),
        }),

        ('Images', {
            'fields': ('preview',),
        }),

        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Extra options. Field archived is for soft delete',
        })

    ]

    def description_shop(self, obj: Product) -> str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + '...'


    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)


        save_csv_products(
            file=form.files['csv_file'].file,
            encoding=request.encoding,
        )
        self.message_user(request, 'Data from CSV was imported')
        return redirect('..')



    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name='import_products_csv',
            )
        ]
        return new_urls + urls


class ProductInLine(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = 'shop_app/orders_changelist.html'
    inlines = [
        ProductInLine,
    ]
    list_display = 'user', 'delivery_address', 'promocode', 'created_in'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) ->str:
        return obj.user.first_name or obj.user.username


    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)


        save_csv_orders(
            file=form.files['csv_file'].file,
            encoding=request.encoding,
        )
        self.message_user(request, 'Data from CSV was imported')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-order-csv/",
                self.import_csv,
                name='import_orders_csv',
            )
        ]
        return new_urls + urls