from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
  UserCreationForm, 
  AuthenticationForm, 
  PasswordChangeForm,
  PasswordResetForm,
  SetPasswordForm,
)
from django.contrib.auth import (
  login, 
  logout, 
  update_session_auth_hash
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse


def signupView(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect(reverse("login"))
  else:
    form = UserCreationForm()
  
  return render(request, "registration/signup.html", {"form": form})


def loginView(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect(reverse("index"))
  else: 
    form  = AuthenticationForm()
  
  return render(request, "registration/login.html", {"form": form})


def logoutView(request):
  logout(request)
  return redirect(reverse("login"))


@login_required
def changePasswordView(request):
  if request.method == "POST":
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request,user)
      return redirect(reverse("password_change_done"))
  else:
    form = PasswordChangeForm(user=request)
    
  return render(request, "registration/change_password.html", {"form": form})


# Step 1: Request reset link
def passwordResetRequestView(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email)
            for user in users:
                # Generate token + uid
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                reset_link = request.build_absolute_uri(
                    reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
                )

                # Send email
                send_mail(
                    "Password Reset",
                    f"Click here to reset your password: {reset_link}",
                    "no-reply@example.com",
                    [email],
                )
            return redirect(reverse("password_reset_done"))
    else:
        form = PasswordResetForm()

    return render(request, "registration/password_reset_form.html", {"form": form})


# Step 2: Confirm link and reset password
def passwordResetConfirmView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse("password_reset_complete"))
        else:
            form = SetPasswordForm(user)
        return render(request, "registration/password_reset_confirm.html", {"form": form})
    else:
        return render(request, "registration/password_reset_invalid.html")