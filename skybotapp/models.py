from django.db import models

# Create your models here.
class botDB(models.Model):
    userId = models.CharField()
    firstLocation = models.CharField()
    secondLocation = models.CharField()
    firstDate = models.DateField()
    secondDate = models.DateField()
  
