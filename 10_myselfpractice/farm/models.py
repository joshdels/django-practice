from django.db import models

class FarmParcel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    area_has = models.FloatField()
    date_created = models.DateField()