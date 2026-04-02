from django.contrib import admin
from .models import PatientRegistration


@admin.register(PatientRegistration)
class PatientRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'file_number', 'full_name', 'email', 'phone', 
        'patient_type', 'gender', 'registration_date', 'is_active'
    ]
    list_filter = ['patient_type', 'gender', 'marital_status', 'is_active', 'registration_date']
    search_fields = ['file_number', 'first_name', 'last_name', 'email', 'phone', 'national_id_no']
    readonly_fields = ['file_number', 'registration_date', 'updated_date', 'age']
    
    fieldsets = (
        ('Registration Info', {
            'fields': ('file_number', 'patient_type', 'registration_date', 'updated_date', 'is_active')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'gender', 'date_of_birth', 'age', 'marital_status', 'nationality')
        }),
        ('Employment & Identification', {
            'fields': ('occupation', 'company', 'national_id_no', 'passport_no')
        }),
        ('Insurance Information', {
            'fields': ('has_health_insurance', 'insurance_company')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Address Information', {
            'fields': ('present_address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Additional Information', {
            'fields': ('how_hear_about_us', 'terms_acknowledged')
        }),
    )
    
    ordering = ['-registration_date']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'
    
    def age(self, obj):
        return obj.age
    age.short_description = 'Age'
