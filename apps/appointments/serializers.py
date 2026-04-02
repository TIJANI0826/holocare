from rest_framework import serializers
from .models import Appointment
from apps.providers.serializers import ProviderSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    patient_display_name = serializers.SerializerMethodField()
    patient_email_display = serializers.SerializerMethodField()
    patient_phone_display = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = (
            'id', 'patient', 'patient_name', 'patient_email', 'patient_phone',
            'patient_display_name', 'patient_email_display', 'patient_phone_display',
            'provider', 'appointment_date', 'start_time', 'end_time',
            'reason', 'notes', 'status', 'is_confirmed', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'patient_display_name', 
                          'patient_email_display', 'patient_phone_display')
    
    def get_patient_display_name(self, obj):
        return obj.get_patient_display_name()
    
    def get_patient_email_display(self, obj):
        return obj.get_patient_email()
    
    def get_patient_phone_display(self, obj):
        return obj.get_patient_phone()


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'patient', 'patient_name', 'patient_email', 'patient_phone',
            'provider', 'appointment_date', 'start_time', 'end_time', 'reason', 'notes'
        )
