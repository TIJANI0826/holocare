from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Web URLs
urlpatterns = [
    path('', views.appointment_booking_view, name='booking'),
    path('confirmation/<int:pk>/', views.booking_confirmation_view, name='booking-confirmation'),
    path('detail/<int:pk>/', views.appointment_detail_view, name='appointment-detail'),
    path('cancel/<int:pk>/', views.cancel_appointment_view, name='cancel-appointment'),
    path('daily/', views.daily_appointments_view, name='daily-appointments'),
    path('daily/<str:date_str>/', views.daily_appointments_view, name='daily-appointments-date'),
    path('monthly/', views.monthly_appointments_view, name='monthly-appointments'),
    path('monthly/<int:year>/<int:month>/', views.monthly_appointments_view, name='monthly-appointments-date'),
]

# API Router for REST endpoints
router = DefaultRouter()
router.register(r'', views.AppointmentViewSet, basename='appointment-api')

api_urlpatterns = [
    path('', include(router.urls)),
]
