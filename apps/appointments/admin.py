from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name_display', 'provider', 'appointment_date', 'start_time', 'status', 'is_confirmed')
    list_filter = ('status', 'appointment_date', 'provider', 'is_confirmed', 'created_at')
    search_fields = ('patient_name', 'patient_email', 'provider__first_name', 'provider__last_name', 'patient__first_name', 'patient__last_name')
    readonly_fields = ('confirmation_token', 'created_at', 'updated_at', 'get_patient_info')
    date_hierarchy = 'appointment_date'
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient', 'patient_name', 'patient_email', 'patient_phone', 'get_patient_info')
        }),
        ('Appointment Details', {
            'fields': ('provider', 'appointment_date', 'start_time', 'end_time', 'reason', 'notes')
        }),
        ('Confirmation & Status', {
            'fields': ('status', 'is_confirmed', 'confirmation_token')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_patient_name_display(self, obj):
        """Display patient name from registered or fallback field."""
        return obj.get_patient_display_name()
    get_patient_name_display.short_description = 'Patient'
    
    def get_patient_info(self, obj):
        """Display patient information."""
        if obj.patient:
            return f"Registered Patient: {obj.patient.full_name} (File #: {obj.patient.file_number})"
        return "Guest/Walk-in Patient"
    get_patient_info.short_description = 'Patient Status'
    
    def save_model(self, request, obj, form, change):
        """Validate before saving."""
        obj.full_clean()
        super().save_model(request, obj, form, change)
