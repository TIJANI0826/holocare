from django.contrib import admin
from .models import Team, Provider


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'get_provider_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'description', 'photo')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_provider_count(self, obj):
        return obj.providers.filter(is_active=True).count()
    get_provider_count.short_description = 'Active Providers'


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'team', 'specialty', 'is_active', 'is_featured', 'email')
    list_filter = ('is_active', 'is_featured', 'specialty', 'team', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'profile_slug')
    prepopulated_fields = {'profile_slug': ('first_name', 'last_name')}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('locations',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'profile_slug', 'photo')
        }),
        ('Professional', {
            'fields': ('specialty', 'team', 'years_of_experience', 'education', 'certifications')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'locations')
        }),
        ('Additional Info', {
            'fields': ('bio', 'languages', 'office_hours'),
            'classes': ('wide',)
        }),
        ('Status & Display', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'
