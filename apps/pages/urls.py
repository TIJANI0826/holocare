from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'pages'

router = DefaultRouter()
router.register(r'pages', views.PageViewSet, basename='page')

urlpatterns = [
    path('', include(router.urls)),
]
