from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class PatientRegistration(models.Model):
    # Patient Type Choices
    PATIENT_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('emergency', 'Emergency'),
        ('direct_billing', 'Direct Billing'),
    ]
    
    # Gender Choices
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    # Marital Status Choices
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    
    # Referral Source Choices
    REFERRAL_SOURCE_CHOICES = [
        ('search_engine', 'Search Engine'),
        ('social_media', 'Social Media'),
        ('referred_by_friend', 'Referred By Friend'),
        ('outreach', 'Outreach'),
        ('others', 'Others'),
    ]
    
    # Basic Information
    file_number = models.CharField(
        max_length=50, 
        unique=True, 
        db_index=True,
        help_text="Unique file number for this patient"
    )
    patient_type = models.CharField(
        max_length=20, 
        choices=PATIENT_TYPE_CHOICES,
        default='regular'
    )
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    
    # Identification
    national_id_no = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="National ID Number"
    )
    passport_no = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Passport Number"
    )
    
    # Insurance Information
    has_health_insurance = models.BooleanField(default=False)
    insurance_company = models.CharField(
        max_length=150, 
        blank=True, 
        null=True,
        help_text="Name of insurance company"
    )
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^[+]?[0-9\s\-()]+$', 'Enter a valid phone number')]
    )
    
    # Address Information
    present_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)
    
    # Contact Information
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^[+]?[0-9\s\-()]+$', 'Enter a valid phone number')]
    )
    email = models.EmailField()
    
    # Referral Information
    how_hear_about_us = models.CharField(
        max_length=50,
        choices=REFERRAL_SOURCE_CHOICES,
        help_text="How did you hear about us?"
    )
    
    # Acknowledgement
    terms_acknowledged = models.BooleanField(
        default=False,
        help_text="Patient acknowledges terms and conditions"
    )
    
    # Metadata
    registration_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-registration_date']
        verbose_name = 'Patient Registration'
        verbose_name_plural = 'Patient Registrations'
        indexes = [
            models.Index(fields=['file_number']),
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['registration_date']),
        ]
    
    def __str__(self):
        return f"{self.file_number} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def save(self, *args, **kwargs):
        # Auto-generate file number if not provided
        if not self.file_number:
            count = PatientRegistration.objects.count()
            self.file_number = f"HMC-{timezone.now().strftime('%Y%m%d')}-{count + 1:04d}"
        super().save(*args, **kwargs)
