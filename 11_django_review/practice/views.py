import hashlib

from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, File
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
            uploaded_file = form.cleaned_data["uploaded_file"]

            # --- Determine the project ---
            selected_project = form.cleaned_data.get("project")
            new_project_name = form.cleaned_data.get("new_project_name")

            if new_project_name:
                # Create or get a new project
                project, _ = Project.objects.get_or_create(
                    name=new_project_name,
                    owner=request.user if request.user.is_authenticated else None,
                )
            elif selected_project:
                # Use existing project
                project = selected_project
            else:
                # Default project
                project, _ = Project.objects.get_or_create(
                    name="default_project",
                    owner=request.user if request.user.is_authenticated else None,
                )

            # --- Determine logical file name and folder ---
            file_name = uploaded_file.name
            file_folder = file_name.replace(" ", "_")

            # --- Compute file hash ---
            file_hash = compute_hash(uploaded_file)

            # --- Check for duplicate within this project only ---
            existing_files = File.objects.filter(
                owner=request.user if request.user.is_authenticated else None,
                project=project,
                hash=file_hash,
            )
            if existing_files.exists():
                form.add_error(
                    "uploaded_file", "This exact file already exists in the project."
                )
            else:
                # --- Determine version number for this file in this project ---
                latest_file = (
                    File.objects.filter(
                        owner=request.user if request.user.is_authenticated else None,
                        project=project,
                        name=file_name,
                    )
                    .order_by("-version")
                    .first()
                )
                version_number = (latest_file.version + 1) if latest_file else 1

                # --- Create the File record ---
                File.objects.create(
                    name=file_name,
                    owner=request.user if request.user.is_authenticated else None,
                    uploaded_file=uploaded_file,
                    hash=file_hash,
                    size=uploaded_file.size,
                    version=version_number,
                    project=project,
                    file_folder=file_folder,
                )

            # --- Re-render form if errors ---
            if form.errors:
                files = File.objects.all()
                return render(request, "rehome.html", {"form": form, "files": files})

            return redirect("rehome")

    else:
        form = ReuploadFileForm()

    # Show all files
    files = File.objects.all()
    return render(request, "rehome.html", {"form": form, "files": files})


def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    if request.method == "POST":
        file.delete()
        return redirect(rehome)
    return redirect(rehome)
