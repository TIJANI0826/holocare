from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Resource, ResourceCategory
from .serializers import ResourceSerializer, ResourceCategorySerializer


class ResourceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for resource categories."""
    queryset = ResourceCategory.objects.all()
    serializer_class = ResourceCategorySerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for resources."""
    queryset = Resource.objects.filter(is_published=True).select_related('category')
    serializer_class = ResourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'file_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'download_count']
    ordering = ['-created_at']
