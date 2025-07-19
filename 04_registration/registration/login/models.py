from django.db import models

# Create your models here.
class UserAccount(models.Model):
  username = models.CharField(max_length=100, null=True, blank=True)
  firstname = models.CharField(max_length=100, null=True, blank=True)
  lastname = models.CharField(max_length=100, null=True, blank=True)
  password = models.CharField(max_length=100, null=True, blank=True)
  email = models.CharField(max_length=200, null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  