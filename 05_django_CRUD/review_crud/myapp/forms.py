from django import forms
from .models import Customer, Products, Photo
from django.forms import inlineformset_factory

class CustomerForm(forms.ModelForm):
  class Meta: 
    model = Customer
    fields = "__all__"
    
# Create inline formset for Products related to Customer
ProductFormSet = inlineformset_factory(
    Customer, Products,
    fields=['item'], extra=1,
)

ImageFormSet = inlineformset_factory(
  Customer, Photo,
  fields = ['image'], extra=5
)