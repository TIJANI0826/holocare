from django import forms
from django.core.validators import RegexValidator
from .models import PatientRegistration


class PatientRegistrationForm(forms.ModelForm):
    # Override fields for better form control
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': True
        }),
        label='Date of Birth'
    )
    
    terms_acknowledged = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='I acknowledge and agree to the terms'
    )
    
    class Meta:
        model = PatientRegistration
        fields = [
            'file_number', 'patient_type', 'first_name', 'last_name', 'gender',
            'marital_status', 'date_of_birth', 'nationality', 'occupation',
            'company', 'national_id_no', 'passport_no', 'has_health_insurance',
            'insurance_company', 'emergency_contact_name', 'emergency_contact_phone',
            'present_address', 'city', 'state', 'postal_code', 'country',
            'phone', 'email', 'how_hear_about_us', 'terms_acknowledged'
        ]
        widgets = {
            'file_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auto-generated if left empty',
                'readonly': True
            }),
            'patient_type': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name',
                'required': True
            }),
            'gender': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
            'marital_status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter nationality',
                'required': True
            }),
            'occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter occupation (optional)',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name (optional)',
            }),
            'national_id_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter national ID number (optional)',
            }),
            'passport_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter passport number (optional)',
            }),
            'has_health_insurance': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={
                'class': 'form-check-input',
            }),
            'insurance_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter insurance company name (if applicable)',
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter emergency contact name',
                'required': True
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter emergency contact phone number',
                'type': 'tel',
                'required': True
            }),
            'present_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your present address',
                'rows': 3,
                'required': True
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city',
                'required': True
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state/province',
                'required': True
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter postal code (optional)',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter country',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
                'type': 'tel',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
                'required': True
            }),
            'how_hear_about_us': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'file_number': 'File Number',
            'patient_type': 'Patient Type',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'gender': 'Gender',
            'marital_status': 'Marital Status',
            'date_of_birth': 'Date of Birth',
            'nationality': 'Nationality',
            'occupation': 'Occupation',
            'company': 'Company',
            'national_id_no': 'National ID No.',
            'passport_no': 'Passport No.',
            'has_health_insurance': 'Do you have health insurance?',
            'insurance_company': 'Insurance Company',
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_phone': 'Emergency Contact Phone No.',
            'present_address': 'Present Address',
            'city': 'City',
            'state': 'State/Province',
            'postal_code': 'Postal Code',
            'country': 'Country',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'how_hear_about_us': 'How did you hear about us?',
            'terms_acknowledged': 'I acknowledge and agree to the terms',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate that if has_health_insurance is True, insurance_company should be filled
        has_insurance = cleaned_data.get('has_health_insurance')
        insurance_company = cleaned_data.get('insurance_company')
        
        if has_insurance and not insurance_company:
            raise forms.ValidationError(
                'Please provide insurance company name if you have health insurance.'
            )
        
        # Validate that at least one ID (National ID or Passport) is provided
        national_id = cleaned_data.get('national_id_no')
        passport = cleaned_data.get('passport_no')
        
        if not national_id and not passport:
            raise forms.ValidationError(
                'Please provide either a National ID Number or Passport Number.'
            )
        
        return cleaned_data
