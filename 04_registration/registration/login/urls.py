from django.urls import path

from . import views

urlpatterns = [
  path("", views.login, name="index"),
  path("check_login/", views.login, name="check_login"),
  path("register/", views.create_account, name="register")
]