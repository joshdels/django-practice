import os
import hashlib

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from .models import Project, File, FileActivity
from .forms import ReuploadFileForm


def compute_hash(uploaded_file):
    hasher = hashlib.sha256()
    for chunk in uploaded_file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()

def unset_latest(user, project, file_name):
    """Helper to unset is_latest for previous files of the same logical file."""
    File.objects.filter(
        owner=user,
        project=project,
        name=file_name,
        is_latest=True,
    ).update(is_latest=False)


def rehome(request):
    user = request.user if request.user.is_authenticated else None

    if request.method == "POST":
        form = ReuploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data["uploaded_file"]

            # --- Determine project ---
            selected_project = form.cleaned_data.get("project")
            new_project_name = form.cleaned_data.get("new_project_name")

            if new_project_name:
                project, _ = Project.objects.get_or_create(
                    name=new_project_name,
                    owner=user,
                    defaults={"is_deleted": False},
                )
            elif selected_project and not selected_project.is_deleted:
                project = selected_project
            else:
                project, _ = Project.objects.get_or_create(
                    name="default_project",
                    owner=user,
                    defaults={"is_deleted": False},
                )

            # 🚫 Block uploads to deleted projects
            if project.is_deleted:
                form.add_error("project", "This project is deleted.")
                return render(request, "rehome.html", {"form": form})

            # --- Prepare file info ---
            file_name = uploaded_file.name
            base_name, _ = os.path.splitext(file_name)
            file_folder = base_name.replace(" ", "_")
            file_hash = compute_hash(uploaded_file)

            with transaction.atomic():
                # --- Check if same file content already exists ---
                existing_same_content = File.objects.filter(
                    owner=user,
                    project=project,
                    name=file_name,
                    hash=file_hash,
                ).first()

                if existing_same_content:
                    # 🔁 Rollback to existing version
                    unset_latest(user, project, file_name)
                    existing_same_content.is_latest = True
                    existing_same_content.save(update_fields=["is_latest"])

                    # Log activity
                    FileActivity.objects.create(
                        file=existing_same_content,
                        user=user,
                        action="reverted"
                    )

                else:
                    # --- Determine version for new upload ---
                    latest_file = File.objects.filter(
                        owner=user,
                        project=project,
                        name=file_name,
                        is_latest=True,
                    ).order_by("-version").first()

                    version_number = (latest_file.version + 1) if latest_file else 1

                    # Unset previous latest version
                    unset_latest(user, project, file_name)

                    # --- Create new file record ---
                    new_file = File.objects.create(
                        name=file_name,
                        owner=user,
                        uploaded_file=uploaded_file,
                        hash=file_hash,
                        size=uploaded_file.size,
                        version=version_number,
                        project=project,
                        file_folder=file_folder,
                        is_latest=True,
                    )

                    # Log activity
                    FileActivity.objects.create(
                        file=new_file,
                        user=user,
                        action="created"
                    )

            return redirect("rehome")

    else:
        form = ReuploadFileForm()

    # Show all non-deleted files with related project to reduce queries
    files = File.objects.select_related("project").filter(project__is_deleted=False)
    projects = Project.objects.all().order_by("-created_at")
    return render(request, "rehome.html", {"form": form, "files": files, "projects": projects})

def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect(rehome)
    return redirect(rehome)

def soft_delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.soft_delete()
        return redirect("rehome")
    return redirect("rehome")
