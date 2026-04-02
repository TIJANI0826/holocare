from django.contrib import admin
from .models import Provider


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'specialty', 'is_active', 'is_featured', 'email')
    list_filter = ('is_active', 'is_featured', 'specialty', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'profile_slug')
    prepopulated_fields = {'profile_slug': ('first_name', 'last_name')}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('locations',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'profile_slug', 'photo')
        }),
        ('Professional', {
            'fields': ('specialty', 'years_of_experience', 'education', 'certifications')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'locations')
        }),
        ('Additional Info', {
            'fields': ('bio', 'languages', 'office_hours'),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'
