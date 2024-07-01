from django.urls import path
from core.views import MainView  #, test_task



urlpatterns = [
    path("", MainView.as_view(), name="home"),
    #path("task/", test_task, name="test_task"),
]