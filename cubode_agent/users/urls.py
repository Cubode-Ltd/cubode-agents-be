from django.urls import path
from users.views import SignupView, LogInAPI, LogOutAPI, check_user

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LogInAPI.as_view(), name='login'),
    path('logout/', LogOutAPI.as_view(), name='logout'),


    path('check/', check_user, name='check'),
]
