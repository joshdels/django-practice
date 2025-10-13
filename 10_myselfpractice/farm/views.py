from django.shortcuts import render, redirect
from django.http import HttpRequest


def homepage(request):
  return render(request, 'farm/home.html')