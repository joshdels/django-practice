from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url


class CustomAccountAdapter(DefaultAccountAdapter):
  def get_signup_redirect_url(self, request):
    return resolve_url("/")