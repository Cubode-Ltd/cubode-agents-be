from django.urls import path
from core.views import MainView, test_task, websocket_test, InferenceAI
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("", MainView.as_view(), name="home"),
    path("task/", test_task, name="test_task"),
    path("socket/", websocket_test, name="websocket_test"),
    path("ai/", InferenceAI.as_view(), name="ai")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

