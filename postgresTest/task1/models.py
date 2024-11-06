from django.db import models

class Pressure(models.Model):
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    date = models.DateTimeField()