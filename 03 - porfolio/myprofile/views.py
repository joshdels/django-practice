from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def myprofile(request):
  return HttpResponse("This is my homepage")

 