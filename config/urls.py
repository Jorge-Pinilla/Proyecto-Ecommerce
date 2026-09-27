"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# 1. Asegúrate de importar store_login_view y store_register_view aquí:
from core.views import (
    superadmin_dashboard, 
    store_front, 
    custom_logout, 
    order_history, 
    store_login_view, 
    store_register_view
)

urlpatterns = [
    path('', lambda request: redirect('/accounts/login/')),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
    path('dashboard/super/', superadmin_dashboard, name='superadmin_dashboard'),
    
    # 2. Rutas de la tienda, login y registro por tienda:
    path('s/<slug:store_slug>/', store_front, name='store_front'),
    path('s/<slug:store_slug>/login/', store_login_view, name='store_login'),
    path('s/<slug:store_slug>/register/', store_register_view, name='store_register'),
    
    path('orders/history/', order_history, name='order_history'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/schema/', login_required(SpectacularAPIView.as_view()), name='schema'),
    path('api/docs/', login_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
]