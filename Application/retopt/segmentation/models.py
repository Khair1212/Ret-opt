from django.db import models
from account.models import Customer


class SegmentedCustomer(models.Model):
  customer_id = models.IntegerField()
  name = models.CharField(max_length=255, default="Customer")
  email = models.EmailField(default="customer@gmail.com")
  cluster_name = models.CharField(max_length=255)
  
  def __str__(self):
    return f"{self.customer_id}: {self.cluster_name}"

class PlotImage(models.Model):
  image = models.ImageField(upload_to='images/', blank=True)

  def __str__(self):
    return f"{self.id}" 
  
  