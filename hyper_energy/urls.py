"""hyper_energy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static

from blog.sitemaps import PostSitemap

sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path("", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("", include(("blog.urls", "blog"), namespace="blog")),
    path("", include(("calculators.urls", "calculators"), namespace="calculators")),
    path("maintenance-supervision/", admin.site.urls),
    # path('orders/', include('orders.urls')),
    path("select2/", include("django_select2.urls")),
    path("search/", include("haystack.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("social-auth/", include("social_django.urls", namespace="social")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
