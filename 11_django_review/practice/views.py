from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import File
from .forms import UploadFileForm


def home(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UploadFileForm()

    files = File.objects.all()

    return render(request, "home.html", {"form": form, "files": files})
