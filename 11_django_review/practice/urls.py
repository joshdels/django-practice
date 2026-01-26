from django.urls import path
from . import views

urlpatterns = [
  path("rehome/", views.rehome, name="rehome"),
  path("rehome/<int:pk>/delete/", views.delete_file, name="delete-file")
]