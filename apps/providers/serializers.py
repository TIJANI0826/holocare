from rest_framework import serializers
from .models import Provider
from apps.core.models import Location, Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ('id', 'name', 'description', 'icon_path')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'city', 'state', 'zip_code', 'phone', 'email', 'map_latitude', 'map_longitude')


class ProviderSerializer(serializers.ModelSerializer):
    specialty = SpecialtySerializer(read_only=True)
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        fields = (
            'id', 'first_name', 'last_name', 'specialty', 'locations',
            'bio', 'photo', 'email', 'phone', 'profile_slug',
            'languages', 'education', 'certifications', 'years_of_experience',
            'is_active', 'is_featured', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
