from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from calendar import monthcalendar, month_name
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Appointment
from .forms import AppointmentBookingForm, AppointmentGuestBookingForm, AppointmentStatusForm
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from apps.providers.models import Provider


# ==================== Web Views ====================

def appointment_booking_view(request):
    """Handle appointment booking for both registered and guest patients."""
    registered_form = AppointmentBookingForm()
    guest_form = AppointmentGuestBookingForm()
    form_type = 'guest'
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'guest')
        
        if form_type == 'registered':
            form = AppointmentBookingForm(request.POST)
            registered_form = form
        else:
            form = AppointmentGuestBookingForm(request.POST)
            guest_form = form
        
        if form.is_valid():
            appointment = form.save(commit=False)
            
            # If registered patient selected, set patient field
            if form_type == 'registered' and form.cleaned_data.get('registered_patient'):
                appointment.patient = form.cleaned_data['registered_patient']
                appointment.patient_name = appointment.patient.full_name
                appointment.patient_email = appointment.patient.email
                appointment.patient_phone = appointment.patient.phone
            
            appointment.save()
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Appointment booked successfully!',
                    'appointment_id': appointment.pk,
                    'confirmation_url': f'/appointments/confirmation/{appointment.pk}/'
                })
            
            messages.success(request, 'Appointment booked successfully! We will confirm your appointment soon.')
            return redirect('appointments:booking-confirmation', pk=appointment.pk)
        else:
            # Collect form errors
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the errors below.',
                    'errors': errors
                }, status=400)
            
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')
    
    providers = Provider.objects.filter(is_active=True)
    context = {
        'registered_form': registered_form,
        'guest_form': guest_form,
        'providers': providers,
        'title': 'Book an Appointment',
        'form_type': form_type,
    }
    return render(request, 'appointments/booking_form.html', context)


def booking_confirmation_view(request, pk):
    """Display booking confirmation page."""
    appointment = get_object_or_404(Appointment, pk=pk)
    context = {
        'appointment': appointment,
        'title': 'Appointment Confirmation',
    }
    return render(request, 'appointments/booking_confirmation.html', context)


def daily_appointments_view(request, date_str=None):
    """Display appointments for a specific day."""
    if date_str:
        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('appointments:daily-appointments')
    else:
        appointment_date = timezone.now().date()
    
    # Filter appointments
    appointments = Appointment.objects.filter(
        appointment_date=appointment_date
    ).select_related('provider', 'patient').order_by('start_time')
    
    # Get provider filter if specified
    provider_id = request.GET.get('provider')
    if provider_id:
        appointments = appointments.filter(provider_id=provider_id)
    
    # Group by provider
    providers = Provider.objects.filter(is_active=True)
    grouped_appointments = {}
    for provider in providers:
        grouped_appointments[provider] = appointments.filter(provider=provider)
    
    context = {
        'appointment_date': appointment_date,
        'today': timezone.now().date(),
        'appointments': appointments,
        'grouped_appointments': grouped_appointments,
        'providers': providers,
        'selected_provider': provider_id,
        'title': f'Appointments - {appointment_date.strftime("%A, %B %d, %Y")}',
    }
    return render(request, 'appointments/daily_appointments.html', context)


def monthly_appointments_view(request, year=None, month=None):
    """Display appointments for a month in calendar view."""
    today = timezone.now().date()
    
    if not year:
        year = today.year
    if not month:
        month = today.month
    
    # Create calendar
    cal = monthcalendar(year, month)
    
    # Get all appointments for this month
    first_day = datetime(year, month, 1).date()
    last_day = datetime(year, month, 1) + timedelta(days=32)
    last_day = (last_day.replace(day=1) - timedelta(days=1)).date()
    
    appointments = Appointment.objects.filter(
        appointment_date__range=[first_day, last_day]
    ).select_related('provider', 'patient')
    
    # Create calendar with appointments
    calendar_with_appointments = []
    for week in cal:
        week_appointments = []
        for day in week:
            if day == 0:
                week_appointments.append({'day': 0, 'appointments': []})
            else:
                date = datetime(year, month, day).date()
                day_appointments = appointments.filter(appointment_date=date)
                week_appointments.append({
                    'day': day,
                    'date': date,
                    'appointments': day_appointments,
                    'is_today': date == today,
                    'status_counts': {
                        'pending': day_appointments.filter(status='pending').count(),
                        'confirmed': day_appointments.filter(status='confirmed').count(),
                        'completed': day_appointments.filter(status='completed').count(),
                        'cancelled': day_appointments.filter(status='cancelled').count(),
                        'no_show': day_appointments.filter(status='no_show').count(),
                    }
                })
        calendar_with_appointments.append(week_appointments)
    
    # Navigation
    current_date = datetime(year, month, 1).date()
    prev_date = (current_date - timedelta(days=1)).replace(day=1)
    next_date = (current_date + timedelta(days=32)).replace(day=1)
    
    context = {
        'year': year,
        'month': month,
        'month_name': month_name[month],
        'today': today,
        'calendar': calendar_with_appointments,
        'prev_year': prev_date.year,
        'prev_month': prev_date.month,
        'next_year': next_date.year,
        'next_month': next_date.month,
        'total_appointments': appointments.count(),
        'title': f'Appointments - {month_name[month]} {year}',
    }
    return render(request, 'appointments/monthly_appointments.html', context)


def appointment_detail_view(request, pk):
    """Display appointment details."""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check if user has permission to view
    # For now, allow access to everyone (you can add permission checks)
    
    context = {
        'appointment': appointment,
        'title': f'Appointment Details - {appointment.get_patient_display_name()}',
    }
    return render(request, 'appointments/appointment_detail.html', context)


def cancel_appointment_view(request, pk):
    """Cancel an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if not appointment.can_cancel():
        messages.error(request, 'This appointment cannot be cancelled.')
        return redirect('appointments:appointment-detail', pk=pk)
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('appointments:booking-confirmation', pk=pk)
    
    context = {
        'appointment': appointment,
        'title': 'Cancel Appointment',
    }
    return render(request, 'appointments/cancel_appointment.html', context)


# ==================== API ViewSet ====================

class AppointmentViewSet(viewsets.ModelViewSet):
    """API viewset for appointments."""
    queryset = Appointment.objects.all().select_related('provider', 'patient')
    serializer_class = AppointmentSerializer
    filterset_fields = ['status', 'provider', 'appointment_date']
    ordering_fields = ['appointment_date', 'created_at']
    ordering = ['-appointment_date']

    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        return AppointmentSerializer

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm appointment."""
        appointment = self.get_object()
        appointment.is_confirmed = True
        appointment.status = 'confirmed'
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel appointment."""
        appointment = self.get_object()
        if appointment.can_cancel():
            appointment.status = 'cancelled'
            appointment.save()
            return Response(AppointmentSerializer(appointment).data)
        return Response(
            {'error': 'This appointment cannot be cancelled'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        """Get appointments by specific date."""
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'error': 'Date parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointments = self.queryset.filter(appointment_date=appointment_date)
            serializer = self.get_serializer(appointments, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_provider_and_date(self, request):
        """Get appointments by provider and date."""
        provider_id = request.query_params.get('provider_id')
        date_str = request.query_params.get('date')
        
        if not provider_id or not date_str:
            return Response(
                {'error': 'provider_id and date parameters required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointments = self.queryset.filter(
                provider_id=provider_id,
                appointment_date=appointment_date
            ).order_by('start_time')
            serializer = self.get_serializer(appointments, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
