from django.urls import path
from core.views import MainView, Registration

from django.urls import path


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path("", MainView.as_view(), name="home"),
    path("register/", Registration.as_view(), name="registration"),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)