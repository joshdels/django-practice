from django.urls import path

from . import views

urlpatterns = [
  path('', views.homepage, name="homepage"),  
  path('contact/', views.contact, name="contact"),
  path('experience/', views.experience, name="experience"),
  path('project/', views.project, name="project")
]