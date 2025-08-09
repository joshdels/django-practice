from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("form/", views.forms_view, name="form"),
  path("load-data/", views.load_data, name="load-data"),
  path("add-data/", views.add_data, name="add-data"),
  path("edit-data/<int:customer_id>/", views.edit_data, name="edit-data"),
  path("delete-data/<int:customer_id>/", views.delete_data, name="delete-data")
]