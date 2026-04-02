from rest_framework import serializers
from .models import BlogPost, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('id', 'name', 'slug', 'description')


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_full_name', read_only=True)
    category = BlogCategorySerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            'id', 'title', 'slug', 'content', 'excerpt', 'featured_image',
            'author', 'category', 'meta_description', 'is_published',
            'published_at', 'view_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'view_count', 'created_at', 'updated_at')
