from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'id', 'slug', 'title', 'content', 'template_name',
            'meta_title', 'meta_description', 'featured_image',
            'is_published', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
