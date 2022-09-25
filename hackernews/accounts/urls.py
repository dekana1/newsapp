from django.urls import path, include
from .views import UserRegisterView, logout_user
from django.contrib.auth import views as auth_views


urlpatterns = [
   
    path("register/", UserRegisterView.as_view(), name="register"),
    path('user_logout/', logout_user, name="logout_user"),
     
]
