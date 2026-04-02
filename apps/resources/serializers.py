from rest_framework import serializers
from .models import Resource, ResourceCategory


class ResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCategory
        fields = ('id', 'name', 'description')


class ResourceSerializer(serializers.ModelSerializer):
    category = ResourceCategorySerializer(read_only=True)

    class Meta:
        model = Resource
        fields = (
            'id', 'title', 'description', 'file', 'category',
            'file_type', 'is_published', 'download_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'download_count', 'created_at', 'updated_at')
