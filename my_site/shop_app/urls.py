
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter



routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)



app_name ='shop_app'
urlpatterns = [
    path('', ShopInfo.as_view(), name='shop'),
    path('api/', include(routers.urls)),

    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetails.as_view(), name='products_details'),
    path('products/<int:pk>/update', ProductUpdate.as_view(), name='product_update'),
    path('products/<int:pk>/delete', ProductDell.as_view(), name='product_delete'),
    path('products/create/', ProductCreate.as_view(), name='create_product'),
    path('products/export/', ProductsDataExportView.as_view(), name='products_export'),
    path('products/latest/feed/', LatestProductsFeed(), name='products_latest_feed'),

    path('order/', OrderList.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('order/<int:pk>/update', OrderUpdate.as_view(), name='order_updates'),
    path('order/<int:pk>/delete', OrderDelete.as_view(), name='order_delete'),
    path('order/create/', CreateOrder.as_view(), name='create_order'),
    path('order/export/', OrderDataExportView.as_view(), name='orders_export'),

    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_orders'),
    path('users/<int:user_id>/orders/export/', UserOrdersExportView.as_view(), name='user_orders_export'),
]
