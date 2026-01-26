import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from .models import File, FileVersion
from .forms import ReuploadFileForm


def compute_hash(uploaded_file):
    hasher = hashlib.sha256()
    for chunk in uploaded_file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()


def rehome(request):
    if request.method == "POST":
        form = ReuploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file_obj = form.cleaned_data.get("file_object")
            new_name = form.cleaned_data.get("new_file_name")
            uploaded_file = form.cleaned_data["uploaded_file"]

            # Create a new File if none selected
            if not file_obj:
                file_obj = File.objects.create(
                    name=new_name,
                    owner=request.user if request.user.is_authenticated else None
                )

            # Compute hash
            file_hash = compute_hash(uploaded_file)

            # Check if this exact file already exists
            if file_obj.versions.filter(hash=file_hash).exists():
                form.add_error("uploaded_file", "This file already exists for this File.")
            else:
                # Get latest version number
                latest_version = file_obj.versions.first()
                version_number = (latest_version.version + 1) if latest_version else 1

                # Create new FileVersion
                FileVersion.objects.create(
                    file=file_obj,
                    uploaded_file=uploaded_file,
                    hash=file_hash,
                    size=uploaded_file.size,
                    version=version_number,
                )

            # If there were errors (duplicate), render form again
            if form.errors:
                files = File.objects.prefetch_related("versions").all()
                return render(request, "rehome.html", {"form": form, "files": files})

            return redirect("rehome")
    else:
        form = ReuploadFileForm()

    files = File.objects.prefetch_related("versions").all()
    return render(request, "rehome.html", {"form": form, "files": files})


def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    if request.method == "POST":
        file.delete()
        return redirect(rehome)
    return redirect(rehome)
