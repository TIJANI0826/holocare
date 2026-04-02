from django.db import models
from django.utils.translation import gettext_lazy as _


class Specialty(models.Model):
    """Medical specialty model for providers."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon_path = models.CharField(max_length=255, blank=True, help_text="Font Awesome icon class or image path")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Specialty')
        verbose_name_plural = _('Specialties')
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(models.Model):
    """Medical clinic location/branch model."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    map_latitude = models.FloatField(null=True, blank=True)
    map_longitude = models.FloatField(null=True, blank=True)
    hours_json = models.JSONField(default=dict, blank=True, help_text="Hours of operation as JSON")
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ['-is_primary', 'name']

    def __str__(self):
        return f"{self.name} - {self.city}"


class Service(models.Model):
    """Medical service model."""
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    icon_path = models.CharField(max_length=255, blank=True)
    duration_minutes = models.IntegerField(default=30, help_text="Service duration in minutes")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='services/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['name']

    def __str__(self):
        return self.name


class FAQ(models.Model):
    """FAQ model for common questions."""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['category', 'order']

    def __str__(self):
        return self.question[:50]
