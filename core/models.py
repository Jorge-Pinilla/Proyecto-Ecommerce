# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils.validators import validate_rut

class User(AbstractUser):
    is_store_admin = models.BooleanField(default=False)
    rut = models.CharField(max_length=12, validators=[validate_rut], unique=True, null=True, blank=True)

class Store(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='managed_store')
    logo = models.ImageField(upload_to='store_logos/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default="#1e293b") # Color CSS personalizado por tienda
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.store.name})"

class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.customer.username} en {self.store.name}"

# core/models.py (Añadir o actualizar estos modelos)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'store') # Un carrito único por usuario para cada tienda

    def __str__(self):
        return f"Carrito de {self.user.username} en {self.store.name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.customer.username} ({self.store.name})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Precio histórico al momento de comprar

    def __str__(self):
        return f"{self.quantity}x {self.product.name if self.product else 'Producto eliminado'} en Orden #{self.order.id}"