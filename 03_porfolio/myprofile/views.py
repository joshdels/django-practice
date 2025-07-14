from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Client, Experience, Project

# Create your views here.
def homepage(request):
  template = loader.get_template('index.html')
  content = {}
  return HttpResponse(template.render(content, request))

def project(request):
  project = Project.objects.all().values
  template = loader.get_template('project.html')
  content = {'projects': project}
  return HttpResponse(template.render(content, request))

def experience(request):
  experience = Experience.objects.all().values
  template = loader.get_template('experience.html')
  content = {'experiences': experience}
  return HttpResponse(template.render(content, request))

def contact(request):
  if request.method == "POST":
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    role = request.POST.get('role')
    
    if Client.objects.filter(email=email).exists():
      return render(request, 'contact.html', {
        'error': 'Email has already been taken.',
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'role': role
    })
    
    Client.objects.create(
      first_name=first_name,
      last_name=last_name,
      email=email,
      position=role
    )
    
    return render(request, 'contact.html', {'success': True})

  return render(request, 'contact.html')

