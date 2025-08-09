from django.db import models

class Customer(models.Model):
  name = models.CharField(max_length=200, null=True, blank=True)
  email = models.EmailField(max_length=200, null=True, blank=True)
  number = models.IntegerField(null=True, blank=True)

