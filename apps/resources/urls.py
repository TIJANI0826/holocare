from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'resources'

router = DefaultRouter()
router.register(r'categories', views.ResourceCategoryViewSet, basename='category')
router.register(r'', views.ResourceViewSet, basename='resource')

urlpatterns = [
    path('', include(router.urls)),
]
