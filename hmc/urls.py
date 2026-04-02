"""
URL Configuration for hmc project.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import SitemapIndex
from apps.appointments import urls as appointments_urls

sitemaps = {
    'index': SitemapIndex(),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Sitemaps
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # API URLs
    path('api/', include('apps.core.urls')),
    path('api/pages/', include('apps.pages.urls')),
    path('api/appointments/', include((appointments_urls.api_urlpatterns, 'appointments'), namespace='appointments-api')),
    path('api/providers/', include('apps.providers.urls')),
    path('api/blog/', include('apps.blog.urls')),
    path('api/resources/', include('apps.resources.urls')),
    
    # Web application URLs
    path('patients/', include('apps.patients.urls')),
    path('appointments/', include((appointments_urls.urlpatterns, 'appointments'), namespace='appointments')),
    
    # Frontend views (should be last)
    path('', include('apps.pages.frontend_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
