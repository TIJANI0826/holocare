from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'blog'

router = DefaultRouter()
router.register(r'categories', views.BlogCategoryViewSet, basename='category')
router.register(r'posts', views.BlogPostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]
