"""algo_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# for media files setting
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from home.sitemaps import StaticViewSitemap
sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("maze/", include("maze.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps})
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
