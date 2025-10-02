from django.shortcuts import HttpResponse, render

from .models import Farm

def index(request):
  farms = Farm.objects.all()
  return render(request, "index.html" , {"farms":farms})
