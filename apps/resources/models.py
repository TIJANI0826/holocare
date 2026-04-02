from django.db import models
from django.utils.translation import gettext_lazy as _


class ResourceCategory(models.Model):
    """Resource category model."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Resource Category')
        verbose_name_plural = _('Resource Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Resource(models.Model):
    """Educational resource model (PDFs, guides, etc.)."""
    title = models.CharField(max_length=300)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    category = models.ForeignKey(ResourceCategory, on_delete=models.PROTECT, related_name='resources')
    file_type = models.CharField(max_length=50, choices=[
        ('pdf', 'PDF'),
        ('doc', 'Document'),
        ('video', 'Video'),
        ('guide', 'Guide'),
        ('other', 'Other'),
    ], default='pdf')
    is_published = models.BooleanField(default=True)
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Resource')
        verbose_name_plural = _('Resources')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
