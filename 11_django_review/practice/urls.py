from django.urls import path
from . import views

urlpatterns = [
  path("rehome/", views.rehome, name="rehome"),
  path("rehome/<int:pk>/delete/", views.delete_project, name="delete-project"),
  path("rehome/<int:pk>/soft-delete", views.soft_delete_project, name="soft-delete-project")
]