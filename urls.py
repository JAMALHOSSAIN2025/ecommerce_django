from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # include your app urls
    path('products/', include('product.urls')), 
    path('api/register/', RegisterView.as_view(), name='register'),
    path('accounts/api/', include('accounts.urls')),  # <-- This line is important
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('order.urls')),
    path('api/products/', include('products.urls')),
    path('api/accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
