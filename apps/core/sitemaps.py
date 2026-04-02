from django.contrib.sitemaps import Sitemap
from apps.pages.models import Page
from apps.blog.models import BlogPost
from apps.providers.models import Provider


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Page.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProviderSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Provider.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class SitemapIndex(Sitemap):
    sitemaps = {
        'pages': PageSitemap,
        'blog': BlogSitemap,
        'providers': ProviderSitemap,
    }

    def location(self, item):
        return f"/sitemap-{item}.xml"
