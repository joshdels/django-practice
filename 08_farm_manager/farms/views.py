from django.shortcuts import HttpResponse
from .models import Farm

def index(request):
  farms = Farm.objects.all()
  farm_names = ", ".join([farm.name for farm in farms])
  return HttpResponse(f"Farms: {farm_names}")