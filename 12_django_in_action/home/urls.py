from django.urls import path
from . import views

urlpatterns = [
  path("", views.credits, name="credits"),
  path("musicians/", views.get_musicians, name="musicians"),
  path("musician/<int:musician_id>/", views.get_musician, name="musician"),
]