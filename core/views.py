from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Store, Product, User, Order

def store_front(request, store_slug):
    """Vista pública para mostrar la tienda y sus productos con diseño independiente"""
    store = get_object_or_404(Store, slug=store_slug)
    products = store.products.all()
    return render(request, 'store_front.html', {'store': store, 'products': products})

@login_required
def superadmin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_store':
            name = request.POST.get('name')
            slug = request.POST.get('slug')
            primary_color = request.POST.get('primary_color', '#1e293b')
            admin_choice = request.POST.get('admin_choice')
            
            if admin_choice == 'existing':
                admin_id = request.POST.get('admin_id')
                admin_user = get_object_or_404(User, id=admin_id)
            else:
                new_username = request.POST.get('new_admin_username')
                new_password = request.POST.get('new_admin_password')
                
                admin_user = User.objects.create_user(
                    username=new_username,
                    password=new_password,
                    is_store_admin=True
                )
            
            Store.objects.create(
                name=name,
                slug=slug,
                primary_color=primary_color,
                admin=admin_user
            )
            return redirect('superadmin_dashboard')

    stores = Store.objects.all()
    store_admins = User.objects.filter(is_store_admin=True)
    all_users = User.objects.all()

    context = {
        'stores': stores,
        'store_admins': store_admins,
        'all_users': all_users,
    }
    return render(request, 'superadmin_dashboard.html', context)

@login_required
def order_history(request):
    """Vista web para mostrar el historial de compras del cliente"""
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def custom_logout(request):
    """Vista personalizada para cerrar sesión de forma segura"""
    logout(request)
    return redirect('/accounts/login/')

# core/views.py (Añadir estas vistas)
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerRegisterForm

def store_login_view(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store_front', store_slug=store.slug)
    else:
        form = AuthenticationForm()
    return render(request, 'store_login.html', {'store': store, 'form': form})

def store_register_view(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente tras registrarse
            return redirect('store_front', store_slug=store.slug)
    else:
        form = CustomerRegisterForm()
    return render(request, 'store_register.html', {'store': store, 'form': form})