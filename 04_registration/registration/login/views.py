from django.shortcuts import render
from django.http import HttpResponse
from .models import UserAccount

# Create your views here.
def login(request):
  return render(request, 'login.html')

def check_logins(request):
  if request.method == 'GET':
    username = request.GET.get('username')
    password = request.GET.get('password')
    remember_me = request.GET.get('remember_me')
      
    db_username = UserAccount.objects.filter(username=username).exists()
    db_password = UserAccount.objects.filter(password=password).exists()
    
    if db_username and db_password: 
      return HttpResponse("Welcome!")
  else:
    return HttpResponse("No records")
  
def create_account(request):
  if request.method == 'GET':
    username = request.GET.get('username')
    firstname = request.GET.get('firstname')
    lastname = request.GET.get('lastname')
    email = request.GET.get('email')
    password = request.GET.get('password')
    
    if username and UserAccount.objects.filter(username__iexact=username).exists():
      print("username taken")
      return HttpResponse("Username already exists")
    elif email and UserAccount.objects.filter(email__iexact=email).exists():
      print("email taken")
      return HttpResponse("Email already exists")
    else:
      
      user = UserAccount(
        username = username,
        firstname = firstname,
        lastname = lastname,
        email = email,
        password = password
      )
      user.save()
      print('sucess')
      return render(request, 'welcome.html')
      
  return render(request, 'register.html')




