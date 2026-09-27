from core.models import User, Store, Product

# 1. Crear el Superadmin general si no existe
super_admin, _ = User.objects.get_or_create(username='superadmin', is_superuser=True, is_staff=True)

# 2. Definir las 4 tiendas solicitadas
store_data = [
    {"name": "TechStore", "slug": "tech", "color": "#0284c7", "products": [("Laptop Pro", 1200.00, 10), ("Mouse Inalámbrico", 25.50, 50)]},
    {"name": "Senderismo Outdoor", "slug": "senderismo", "color": "#16a34a", "products": [("Mochila de Trekking 50L", 85.00, 15), ("Botas impermeables", 110.00, 20)]},
    {"name": "MusicWorld", "slug": "musica", "color": "#9333ea", "products": [("Guitarra Acústica", 200.00, 8), ("Audífonos de Estudio", 75.00, 30)]},
    {"name": "Esencia Perfumes", "slug": "perfumes", "color": "#db2777", "products": [("Perfume Amaderado 100ml", 60.00, 25), ("Fragancia Floral", 50.00, 40)]},
]

for data in store_data:
    # Crear un usuario administrador específico para cada tienda
    store_user, _ = User.objects.get_or_create(username=f"admin_{data['slug']}", is_store_admin=True)
    
    # Crear la tienda asociada
    store, _ = Store.objects.get_or_create(
        slug=data['slug'], 
        defaults={'name': data['name'], 'admin': store_user, 'primary_color': data['color']}
    )
    
    # Poblar productos iniciales
    for prod_name, price, stock in data['products']:
        Product.objects.get_or_create(store=store, name=prod_name, defaults={'price': price, 'stock': stock})

print("¡Las 4 tiendas y sus inventarios se han creado exitosamente!")