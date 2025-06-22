from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView 
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('accounts/', include('accounts.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API endpoints
    path('api/products/', include('products.api_urls')),  # ✅ Simple and clean
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/orders-alt/', include('order_app.urls')),

    # Fallback homepage or root
    path('', include('accounts.urls')),

    path('', RedirectView.as_view(url='/home/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
