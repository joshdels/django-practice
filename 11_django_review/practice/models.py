import os
from django.db import models
from django.conf import settings
from django.db.models import Q, UniqueConstraint


def file_upload_path(instance, filename):
    base_name, ext = os.path.splitext(filename)
    user_id = instance.owner.id if instance.owner else "anon"
    project_name = instance.project.name if instance.project else "default_project"
    file_folder = instance.file_folder or base_name.replace(" ", "_")
    return f"uploads/{user_id}/{project_name}/{file_folder}/{base_name}_v{instance.version}{ext}"


class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    uploaded_file = models.FileField(upload_to=file_upload_path)
    hash = models.CharField(max_length=64, db_index=True)
    size = models.PositiveBigIntegerField()
    version = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_latest = models.BooleanField(default=False, db_index=True)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )

    file_folder = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["owner", "project", "name"],
                condition=Q(is_latest=True),
                name="one_latest_file_per_logical_file",
            )
        ]

    def __str__(self):
        return f"{self.name} v{self.version}"
