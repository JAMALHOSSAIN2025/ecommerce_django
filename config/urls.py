from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # UI Views (HTML pages)
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # API Views (JWT, Register, Complete Profile, etc.)
    path('api/accounts/', include('accounts.api_urls')),  # REST API endpoints

    # Social Login (Google, etc.)
    path('social-auth/', include('social_django.urls', namespace='social')),
]

# Serve media files during development (only when DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
