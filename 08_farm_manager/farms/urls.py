from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("add/", views.addFarmView, name="add"),
  path("<int:id>/", views.listView, name="list"),
  path("edit/<int:id>", views.editView, name="edit"),
  path("delete/<int:id>/", views.deleteView, name="delete"),
]