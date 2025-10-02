from django.contrib import admin
from django.urls import include, path
from farms import views


urlpatterns = [
    path("", views.index, name="index"),
    path("farms/", include("farms.urls")),
    path("admin/", admin.site.urls),
]
