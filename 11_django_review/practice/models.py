from django.db import models
from django.conf import settings


class File(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name
    

class FileVersion(models.Model):
    file  = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        related_name='versions',
        null=True,
        blank=True
    )
    uploaded_file = models.FileField(upload_to="uploads/%Y/%m/")
    hash = models.CharField(max_length=64, db_index=True)
    size = models.PositiveBigIntegerField()
    version = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ("file", "hash")
        ordering = ["-version"]

    def __str__(self):
        return f"{self.file.name} v{self.version}"


    

