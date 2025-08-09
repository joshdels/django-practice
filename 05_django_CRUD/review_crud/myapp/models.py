from django.db import models

class Customer(models.Model):
  name = models.CharField(max_length=200, null=True, blank=True)
  email = models.EmailField(max_length=200, null=True, blank=True)
  number = models.IntegerField(null=True, blank=True)
  
  def __str__(self):
    return f"{self.name}, {self.email}, {self.number}"
  
class Products(models.Model):
  item = models.CharField(max_length=300, null=True, blank=True)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='products')

class Photo(models.Model):
  image = models.ImageField(upload_to='customer_photos/', null=True, blank=True)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='photos')