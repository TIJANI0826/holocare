from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.providers.models import Provider
from apps.patients.models import PatientRegistration


class Appointment(models.Model):
    """Appointment booking model."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    # Link to registered patient (optional for walk-ins)
    patient = models.ForeignKey(
        PatientRegistration, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='appointments'
    )
    
    # Fallback fields for non-registered patients/walk-ins
    patient_name = models.CharField(max_length=200)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=20)
    
    # Appointment details
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, related_name='appointments')
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.TextField()
    notes = models.TextField(blank=True)
    
    # Status and confirmation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confirmation_token = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')
        ordering = ['-appointment_date', 'start_time']
        indexes = [
            models.Index(fields=['provider', 'appointment_date']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['patient', 'appointment_date']),
        ]

    def __str__(self):
        return f"{self.get_patient_display_name()} - {self.provider.get_full_name()} ({self.appointment_date})"

    def get_patient_display_name(self):
        """Get patient name from registered patient or fallback fields."""
        if self.patient:
            return self.patient.full_name
        return self.patient_name
    
    def get_patient_email(self):
        """Get patient email from registered patient or fallback field."""
        if self.patient:
            return self.patient.email
        return self.patient_email
    
    def get_patient_phone(self):
        """Get patient phone from registered patient or fallback field."""
        if self.patient:
            return self.patient.phone
        return self.patient_phone

    def clean(self):
        if self.appointment_date and self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError({'end_time': 'End time must be after start time.'})
            
            # Check for overlapping appointments with the same provider
            overlapping = Appointment.objects.filter(
                provider=self.provider,
                appointment_date=self.appointment_date,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            ).exclude(pk=self.pk)
            
            if overlapping.exists():
                raise ValidationError('This provider has a conflicting appointment at this time.')
    
    def is_past(self):
        """Check if appointment date is in the past."""
        return self.appointment_date < timezone.now().date()
    
    def can_cancel(self):
        """Check if appointment can be cancelled."""
        return self.status not in ['completed', 'cancelled']
