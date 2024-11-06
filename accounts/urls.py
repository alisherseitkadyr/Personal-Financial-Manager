from django.urls import path
from .views import UserFactory

urlpatterns = [
    path("register/", UserFactory.create_user_view("register"), name="register"),
    path("login/", UserFactory.create_user_view("login"), name="login"),
]
