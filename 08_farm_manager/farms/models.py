from django.db import models

# Create your models here.
class Farm(models.Model):
  location = models.CharField(max_length=50, blank=True, null=True)
  name = models.CharField(max_length=50, blank=True, null=True)
  
  def __str__(self):
    return self.name  