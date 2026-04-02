from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import FAQ, Location, Service, Specialty


@api_view(['GET'])
def api_overview(request):
    """API overview endpoint."""
    return Response({
        'status': 'API is running',
        'version': '1.0.0',
        'endpoints': {
            'pages': '/api/pages/',
            'appointments': '/api/appointments/',
            'providers': '/api/providers/',
            'blog': '/api/blog/',
            'resources': '/api/resources/',
        }
    })
