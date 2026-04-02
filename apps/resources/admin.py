from django.contrib import admin
from .models import Resource, ResourceCategory


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'file_type', 'is_published', 'download_count')
    list_filter = ('is_published', 'file_type', 'category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('download_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'file')
        }),
        ('Organization', {
            'fields': ('category', 'file_type')
        }),
        ('Status', {
            'fields': ('is_published', 'download_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
