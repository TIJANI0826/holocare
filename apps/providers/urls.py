from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'providers'

router = DefaultRouter()
router.register(r'', views.ProviderViewSet, basename='provider')

urlpatterns = [
    path('', include(router.urls)),
]
