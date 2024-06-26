from django.urls import path
from core.views import MainView


urlpatterns = [
    path("", MainView.as_view(), name="home"),
]
