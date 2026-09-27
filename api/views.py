from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Store, Product, Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, OrderHistorySerializer

class CartDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, store_slug):
        store = get_object_or_404(Store, slug=store_slug)
        cart, _ = Cart.objects.get_or_create(user=request.user, store=store)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request, store_slug):
        store = get_object_or_404(Store, slug=store_slug)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id, store=store)
        cart, _ = Cart.objects.get_or_create(user=request.user, store=store)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, store_slug):
        store = get_object_or_404(Store, slug=store_slug)
        cart = get_object_or_404(Cart, user=request.user, store=store)
        
        items = cart.items.all()
        if not items:
            return Response({"error": "El carrito está vacío."}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.product.price * item.quantity for item in items)

        order = Order.objects.create(
            store=store,
            customer=request.user,
            total=total
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Vaciar el carrito después de la compra
        cart.items.all().delete()

        serializer = OrderHistorySerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, store_slug):
        store = get_object_or_404(Store, slug=store_slug)
        orders = Order.objects.filter(customer=request.user, store=store).order_by('-created_at')
        serializer = OrderHistorySerializer(orders, many=True)
        return Response(serializer.data)