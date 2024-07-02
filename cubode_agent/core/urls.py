from django.urls import path
from core.views import MainView, test_task, websocket_test



urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("task/", test_task, name="test_task"),
    path("socket/", websocket_test, name="websocket_test"),
]