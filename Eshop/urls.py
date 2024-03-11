from django.contrib import admin
from django.urls import path  , include
from django.conf.urls.static import static
from . import settings

# Import necessary modules from drf-yasg
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Define Schema view
schema_view = get_schema_view(
    openapi.Info(
        title="EShop API",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),

    # Add drf-yasg URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
