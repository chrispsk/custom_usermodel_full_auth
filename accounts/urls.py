from django.contrib import admin
from django.urls import path
from .views import home, user_login, user_logout, register, activate_user


urlpatterns = [
    path('register/', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('activate/<code>/', activate_user),
]
