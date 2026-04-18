from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Page
from apps.providers.models import Provider


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for pages."""
    queryset = Page.objects.filter(is_published=True)
    lookup_field = 'slug'

    def get_serializer_class(self):
        from .serializers import PageSerializer
        return PageSerializer


def page_detail(request, slug):
    """Frontend view for page detail with fallback to static templates."""
    # Try to get page from database
    try:
        page = Page.objects.get(slug=slug, is_published=True)
        template_name = f'pages/{page.template_name}.html'
        context = {'page': page}
    except Page.DoesNotExist:
        # Fallback to static template if not in database
        # This allows pages to work without database entries during development
        static_pages = {
            'home': 'pages/home.html',
            'about': 'pages/about.html',
            'services': 'pages/services.html',
            'contact': 'pages/contact.html',
            'providers': 'pages/providers.html',
            'appointments': 'pages/appointments.html',
            'blog': 'pages/blog.html',
            'resources': 'pages/resources.html',
            'faq': 'pages/faq.html',
            'gallery': 'pages/gallery.html',
            'media': 'pages/media.html',
        }
        
        if slug not in static_pages:
            raise Http404(f"Page '{slug}' not found")
        
        template_name = static_pages[slug]
        context = {'slug': slug, 'page': None}
    
    # Add providers context for appointments page
    if slug == 'appointments':
        context['providers'] = Provider.objects.filter(is_active=True)
    
    return render(request, template_name, context)


def home(request):
    """Frontend home page view."""
    try:
        page = Page.objects.get(slug='home', is_published=True)
        context = {'page': page}
    except Page.DoesNotExist:
        context = {'slug': 'home', 'page': None}
    
    return render(request, 'pages/home.html', context)

