from django.db import models

# Create your models here.
class botDB(models.Model):
    userId = models.CharField(max_length = 100)
    firstLocation = models.CharField(max_length = 100)
    secondLocation = models.CharField(max_length = 100)
    firstDate = models.DateField(max_length = 100)
    secondDate = models.DateField(max_length = 100)
  
