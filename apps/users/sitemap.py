from django.contrib.auth import get_user_model
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from . import models

User = get_user_model()

class UserSitemap(Sitemap):
    def items(self):
        return models.User.objects.filter(is_active=True)

    def priority(self, obj):
        return 0.8

    def changefreq(self, obj):
        return "always"

    def location(self, obj):
        return reverse('users:profile', kwargs={'id': obj.pk})