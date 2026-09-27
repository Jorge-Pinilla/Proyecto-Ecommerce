# api/serializers.py
from rest_framework import serializers
from core.models import Product, Order, Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'slug', 'primary_color', 'logo']

class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'store', 'name', 'price', 'stock']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'store', 'customer', 'total', 'created_at']
        read_only_fields = ['customer', 'total']

# api/serializers.py (Añadir al archivo existente)
from core.models import Cart, CartItem, OrderItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    total_cart = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'store', 'store_name', 'items', 'total_cart', 'updated_at']

    def get_total_cart(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'price']

class OrderHistorySerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'store_name', 'total', 'created_at', 'items']

