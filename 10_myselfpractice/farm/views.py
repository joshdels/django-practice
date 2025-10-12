from django.shortcuts import render, redirect
from django.http import HttpResponse


def homepage(request):
  return HttpResponse("Hello")
  return render(request, 'farm/home.html')