from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import Specialty, Location
from django.core.validators import URLValidator


class Provider(models.Model):
    """Doctor/Healthcare Provider model."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name='providers')
    locations = models.ManyToManyField(Location, related_name='providers')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='providers/', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    office_hours = models.JSONField(default=dict, blank=True, help_text="Office hours as JSON")
    profile_slug = models.SlugField(unique=True)
    languages = models.CharField(max_length=300, blank=True, help_text="Comma-separated language list")
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['is_active', '-is_featured']),
            models.Index(fields=['specialty']),
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return f"/providers/{self.profile_slug}/"
