from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from . import models


class ThingSitemap(Sitemap):
    def items(self):
        return models.Thing.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def priority(self, obj):
        return 0.8

    def changefreq(self, obj):
        return "always"

    def location(self, obj):
        return reverse('things:detail', kwargs={'pk': obj.pk})