from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Customer
from .forms import CustomerForm
from django.views.decorators.csrf import csrf_exempt


def index(request):
  customers = Customer.objects.all()
  return render(request, 'customers.html', {"customers":customers})

def forms_view(request):
    return render(request, 'add_forms.html')

def load_data(request):
  customers = Customer.objects.all()
  return render(request, "customers.html", {"customers":customers})


@csrf_exempt
def add_data(request):
  if request.method == "POST":
    form = CustomerForm(request.POST)  
    if form.is_valid():
      form.save()
      return redirect("load-data")
  else:
    form = CustomerForm()
  return render(request, 'add_forms.html', {'form': form})

    
def edit_data(request, customer_id):
  customer = get_object_or_404(Customer, id=customer_id)
  
  if request.method == 'POST':
    form = CustomerForm(request.POST, instance=customer)
    if form.is_valid():
      form.save()
      return redirect('load-data')
  else:
    form = CustomerForm(instance=customer)
      
    return render(request, 'edit_forms.html', {'form': form, 'customer': customer})
    

def delete_data(request, customer_id):
  customer = get_object_or_404(Customer, id=customer_id)
  customer.delete()
  return redirect('load-data')