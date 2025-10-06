from django.urls import path
from . import views

urlpatterns = [
  path("change-password", views.changePasswordView, name="change-password"),
  path("password-reset", views.passwordResetRequestView,name="password-reset"),
  path("password-reset-confirm", views.changePasswordView, name="password-reset-confirm"),
  path("password_change_done", views.passwordResetConfirmView, name="password-reset-confirm"),
]

 