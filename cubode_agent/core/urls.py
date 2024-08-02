from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from core.views import MainView

urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
