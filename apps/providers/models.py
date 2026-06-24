from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import Specialty, Location
from django.core.validators import URLValidator


class Team(models.Model):
    """Healthcare team/department model."""
    name = models.CharField(max_length=200, help_text="Team or department name")
    position = models.CharField(max_length=200, help_text="Position or role of the team within the organization", blank=True)
    description = models.TextField(blank=True, help_text="Team description and overview")
    photo = models.ImageField(upload_to='teams/', blank=True, help_text="Team group photo")
    order = models.IntegerField(default=0, help_text="Display order on providers page")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'order']),
        ]

    def __str__(self):
        return self.name


class Provider(models.Model):
    """Doctor/Healthcare Provider model."""
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name='providers')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='providers', help_text="Team or department this provider belongs to")
    locations = models.ManyToManyField(Location, related_name='providers',null=True,blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='providers/', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    office_hours = models.JSONField(default=dict, blank=True, help_text="Office hours as JSON")
    profile_slug = models.SlugField(unique=True)
    languages = models.CharField(max_length=300, blank=True, help_text="Comma-separated language list")
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Display order within team")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')
        ordering = ['team__order', 'team__name', 'order', 'last_name', 'first_name']
        indexes = [
            models.Index(fields=['is_active', '-is_featured']),
            models.Index(fields=['specialty']),
            models.Index(fields=['team', 'is_active']),
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return f"/providers/{self.profile_slug}/"
