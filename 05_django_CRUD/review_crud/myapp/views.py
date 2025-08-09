from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Customer
from .forms import CustomerForm, ProductFormSet, ImageFormSet
from django.views.decorators.csrf import csrf_exempt



def index(request):
  customers = Customer.objects.prefetch_related("products", "photos")
  return render(request, 'customers.html', {"customers":customers})

def load_data(request):
  customers = Customer.objects.prefetch_related("products", "photos")
  return render(request, "customers.html", {"customers":customers})

def forms_view(request):
    return render(request, 'add_forms.html')

def add_data(request):
  if request.method == "POST":
    form = CustomerForm(request.POST, request.FILES)  
    if form.is_valid():
      customer = form.save()
      formset = ProductFormSet(request.POST, instance=customer)
      imageset = ImageFormSet(request.POST, request.FILES, instance=customer)
      if formset.is_valid() and imageset.is_valid():
        formset.save()
        imageset.save()
        return redirect("load-data")
    else:
      formset = ProductFormSet()
      imageset = ImageFormSet()
  else:
    form = CustomerForm()
    formset = ProductFormSet()
    imageset = ImageFormSet()
  return render(request, 'add_forms.html', {'form': form, 'formset': formset, 'imageset': imageset})

    
def edit_data(request, customer_id):
  customer = get_object_or_404(Customer, id=customer_id)
  
  if request.method == 'POST':
    form = CustomerForm(request.POST, request.FILES, instance=customer)
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