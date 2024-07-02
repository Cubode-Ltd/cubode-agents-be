from django.urls import path
from core.views import MainView  #, test_task
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("", MainView.as_view(), name="home"),
    #path("task/", test_task, name="test_task"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

