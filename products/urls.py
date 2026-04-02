from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    CartView,
    CartDeleteView,
    OrderView,
    OrderDetailView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartDeleteView.as_view(), name='cart-delete'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]