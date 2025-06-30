from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import RegisterView  # ✅ এই লাইনটি যোগ করুন

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Authentication (Traditional and Social)
    path('accounts/', include('accounts.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('api/register/', RegisterView.as_view(), name='register'),

    # JWT Token Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API Endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.api_urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/orders-alt/', include('order_app.urls')),

    # Default fallback or root redirect
    path('', RedirectView.as_view(url='/home/', permanent=False)),
]

# Media files (for development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
