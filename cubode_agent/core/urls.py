from django.urls import path, include
from django.contrib import admin
from core.views import MainView, Registration, Login
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path("register/", Registration.as_view(), name="registration"),
    path("login/", Login.as_view(), name="login"),
    path("auth/", include("authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)
