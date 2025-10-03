from django.shortcuts import redirect, render, get_object_or_404

from .models import Farm
from .forms import FarmForm

def index(request):
  farms = Farm.objects.all()
  return render(request, "index.html" , {"farms":farms})


def addFarmView(request):
  if request.method == "POST":
    form = FarmForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('index')
  else:
    form = FarmForm()
  return render(request, "farm_form.html", {"form": form})
        
         
def listView(request, id):
  farm = Farm.objects.get(id=id)
  return render(request, "detail_view.html", {"farm":farm})


def editView(request, id):
  farm = get_object_or_404(Farm, id=id)
  
  if request.method == "POST":
    form = FarmForm(request.POST, instance=farm)
    if form.is_valid():
      form.save()
      return redirect("index")
  else:
    form = FarmForm(instance=farm)
    
  return render(request, "edit_view.html", {"form": form})


def deleteView(request, id):
  farm = get_object_or_404(Farm, id=id)
  if request.method == "POST":
    farm.delete()
    return redirect("/")