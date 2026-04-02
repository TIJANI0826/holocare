from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogPost, BlogCategory
from .serializers import BlogPostSerializer, BlogCategorySerializer


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for blog categories."""
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    lookup_field = 'slug'


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for blog posts."""
    queryset = BlogPost.objects.filter(is_published=True).select_related('author', 'category')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['published_at', 'view_count', 'created_at']
    ordering = ['-published_at']
