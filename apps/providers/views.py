from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Provider
from .serializers import ProviderSerializer


class ProviderViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for providers."""
    queryset = Provider.objects.filter(is_active=True).select_related('specialty').prefetch_related('locations')
    serializer_class = ProviderSerializer
    lookup_field = 'profile_slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialty', 'locations', 'is_featured']
    search_fields = ['first_name', 'last_name', 'specialty__name']
    ordering_fields = ['first_name', 'last_name', 'created_at']
    ordering = ['-is_featured', 'last_name']
