from core.views import MainView, InferenceAI, WebSocketTest, HtmxTest

from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from core.views import MainView
import os 

urlpatterns = [
    
    path("", MainView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    
    path("socket/", WebSocketTest.as_view(), name="websocket_test"),
    path("ai/", InferenceAI.as_view(), name="ai"),
    path("htmx_socket/", HtmxTest.as_view(), name="HtmxTest")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
