from django.urls import path
from . import views

urlpatterns = [
  path("signup/", views.signupView, name="signup"),
  path("login/", views.loginView, name="login"),
  path("logout/", views.logoutView, name="logout"),
  path("change-password", views.changePasswordView, name="change-password"),
  path("password-reset-confirm", views.changePasswordView, name="password-reset-confirm"),
  path("password_change_done", views.passwordResetConfirmView, name="password-reset-confirm"),
  
]

 