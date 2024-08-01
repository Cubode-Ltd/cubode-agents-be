from django.urls import path, re_path, include
from django.contrib import admin
from core.views import MainView, Registration, Login, RecoverPassword
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    re_path(r"^register/?$", Registration.as_view(), name="registration"),
    re_path(r"^login/?$", Login.as_view(), name="login"),
    re_path(r"^recover_password/?$", RecoverPassword.as_view(), name="recover-password"),
    path("auth/", include("authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
