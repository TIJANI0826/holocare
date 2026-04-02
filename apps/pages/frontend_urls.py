from django.urls import path
from . import views

app_name = 'pages_frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>/', views.page_detail, name='page-detail'),
]
