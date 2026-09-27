# api/urls.py
from django.urls import path
from .views import CartDetailView, CheckoutView, OrderHistoryListView

urlpatterns = [
    path('stores/<slug:store_slug>/cart/', CartDetailView.as_view(), name='cart-detail'),
    path('stores/<slug:store_slug>/checkout/', CheckoutView.as_view(), name='cart-checkout'),
    path('orders/history/', OrderHistoryListView.as_view(), name='order-history'),
]