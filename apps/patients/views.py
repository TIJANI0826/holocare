from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.conf import settings
from .models import PatientRegistration
from .forms import PatientRegistrationForm


def patient_registration_view(request):
    """Handle patient registration form submission"""
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            
            # Send confirmation email
            send_registration_email(patient)
            
            messages.success(
                request, 
                f'Registration successful! Your file number is: {patient.file_number}. A confirmation email has been sent to {patient.email}.'
            )
            return redirect('patients:registration-success', pk=patient.pk)
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PatientRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Patient Registration',
    }
    return render(request, 'patients/registration_form.html', context)


def send_registration_email(patient):
    """Send registration confirmation email to patient"""
    try:
        subject = 'Welcome to Habib Medical Hospital - Registration Confirmation'
        
        # Prepare email context
        context = {
            'patient_name': patient.full_name,
            'file_number': patient.file_number,
            'registration_date': patient.registration_date,
            'clinic_email': 'info@holcare.com',
            'clinic_phone': '+234 805 544 4565',
            'clinic_address': '1B Rudolf Street, Maitama, FCT, Abuja, Nigeria',
        }
        
        # Render email template
        html_message = render_to_string('patients/registration_email.html', context)
        plain_message = f"""
Dear {patient.full_name},

Thank you for registering with Holcare Health & Wellness Clinic!

Your File Number: {patient.file_number}

We are delighted to have you as a valued patient. Our team is committed to providing you with exceptional healthcare services.

If you have any questions or need to reschedule your appointment, please feel free to contact us:
- Email: info@holcare.com
- Phone: +234 805 544 4565

Best regards,
Holcare Health & Wellness Clinic Team
1B Rudolf Street, Maitama, FCT, Abuja, Nigeria
        """
        
        # Send email
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [patient.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email to {patient.email}: {str(e)}")
        # Don't raise error, just log it - registration should still succeed


def registration_success_view(request, pk):
    """Display registration success page"""
    try:
        patient = PatientRegistration.objects.get(pk=pk)
    except PatientRegistration.DoesNotExist:
        messages.error(request, 'Patient registration not found.')
        return redirect('patients:registration')
    
    context = {
        'patient': patient,
        'title': 'Registration Successful',
    }
    return render(request, 'patients/registration_success.html', context)


def patient_list_view(request):
    """List all patient registrations (Admin view)"""
    patients = PatientRegistration.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        from django.db.models import Q
        patients = patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(file_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    context = {
        'patients': patients,
        'search_query': search_query,
        'title': 'Patient List',
    }
    return render(request, 'patients/patient_list.html', context)


def patient_detail_view(request, pk):
    """Display detailed patient information"""
    try:
        patient = PatientRegistration.objects.get(pk=pk)
    except PatientRegistration.DoesNotExist:
        messages.error(request, 'Patient not found.')
        return redirect('patients:patient-list')
    
    context = {
        'patient': patient,
        'title': f'Patient Details - {patient.full_name}',
    }
    return render(request, 'patients/patient_detail.html', context)
