"""LostAndFoundSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.static import serve
import settings
from apps.things.sitemap import ThingSitemap
from apps.users.sitemap import UserSitemap

sitemaps = {
    'ThingSitemap': ThingSitemap,
    'UserSitemap': UserSitemap,
}
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.things.urls', namespace='things')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'.txt$', serve, {'document_root': settings.STATIC_ROOT, 'path': "robots.txt"}),
] + debug_toolbar_urls()

handler404 = 'apps.things.views.view_404'
handler500 = 'apps.things.views.view_500'