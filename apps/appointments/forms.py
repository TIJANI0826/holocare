from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Appointment
from apps.patients.models import PatientRegistration
from apps.providers.models import Provider


class AppointmentBookingForm(forms.ModelForm):
    """Form for booking new appointments."""
    
    # Optional patient selection for registered patients
    registered_patient = forms.ModelChoiceField(
        queryset=PatientRegistration.objects.filter(is_active=True).order_by('-registration_date'),
        required=False,
        label='Select Registered Patient (Optional)',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_registered_patient'
        })
    )
    
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.now().date().isoformat(),
        }),
        label='Appointment Date'
    )
    
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
        label='Start Time'
    )
    
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
        label='End Time'
    )

    class Meta:
        model = Appointment
        fields = ['provider', 'appointment_date', 'start_time', 'end_time', 'reason', 'notes']
        widgets = {
            'provider': forms.Select(attrs={
                'class': 'form-control',
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your reason for the appointment'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active providers
        self.fields['provider'].queryset = Provider.objects.filter(is_active=True)
        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        appointment_date = cleaned_data.get('appointment_date')
        
        # Validate time range
        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError('End time must be after start time.')
        
        # Validate appointment is not in the past
        if appointment_date:
            if appointment_date < timezone.now().date():
                raise ValidationError('Appointment date cannot be in the past.')
        
        return cleaned_data


class AppointmentGuestBookingForm(forms.ModelForm):
    """Form for guest appointments (non-registered patients)."""
    
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.now().date().isoformat(),
        }),
        label='Appointment Date'
    )
    
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
        label='Start Time'
    )
    
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
        label='End Time'
    )

    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient_email', 'patient_phone', 'provider', 
                  'appointment_date', 'start_time', 'end_time', 'reason', 'notes']
        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name'
            }),
            'patient_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'patient_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'provider': forms.Select(attrs={
                'class': 'form-control',
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your reason for the appointment'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active providers
        self.fields['provider'].queryset = Provider.objects.filter(is_active=True)
        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        appointment_date = cleaned_data.get('appointment_date')
        
        # Validate time range
        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError('End time must be after start time.')
        
        # Validate appointment is not in the past
        if appointment_date:
            if appointment_date < timezone.now().date():
                raise ValidationError('Appointment date cannot be in the past.')
        
        return cleaned_data


class AppointmentStatusForm(forms.ModelForm):
    """Form for updating appointment status (admin/staff use)."""
    
    class Meta:
        model = Appointment
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes'
            }),
        }
