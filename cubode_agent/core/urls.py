from django.urls import path
from core.views import MainView, InferenceAI, WebSocketTest, HtmxTest
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("", MainView.as_view(), name="home"),
    path("socket/", WebSocketTest.as_view(), name="websocket_test"),
    path("ai/", InferenceAI.as_view(), name="ai"),
    path("htmx_socket/", HtmxTest.as_view(), name="HtmxTest")
]

urlpatterns #+= htmx_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

