from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Page(models.Model):
    """CMS Page model for managing site pages."""
    TEMPLATE_CHOICES = [
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
        ('providers', 'Providers'),
        ('contact', 'Contact'),
        ('default', 'Default'),
    ]

    slug = models.SlugField(unique=True, max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="HTML content allowed")
    template_name = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='default')
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO title tag")
    meta_description = models.CharField(max_length=300, blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=300, blank=True, help_text="SEO keywords")
    canonical_url = models.URLField(blank=True, help_text="Canonical URL for SEO")
    is_published = models.BooleanField(default=True)
    featured_image = models.ImageField(upload_to='pages/', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_pages')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_pages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.slug}/"
