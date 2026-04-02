from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('register/', views.patient_registration_view, name='registration'),
    path('registration-success/<int:pk>/', views.registration_success_view, name='registration-success'),
    path('list/', views.patient_list_view, name='patient-list'),
    path('detail/<int:pk>/', views.patient_detail_view, name='patient-detail'),
]
