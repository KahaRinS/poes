import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name

class Sensors(models.Model):
    senname = models.CharField(max_length=80, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='regions')
    dolgitude = models.CharField(max_length=80, blank=False)
    longitude = models.CharField(max_length=80, blank=False)

    def __str__(self):
        return self.senname


class Results(models.Model):
    # temp = models.CharField(max_length=80, unique=True)
    temp = models.IntegerField(null=True)
    sensor = models.ForeignKey(Sensors, on_delete=models.CASCADE, related_name='sens')
    date = models.DateField(blank=False)
    time = models.TimeField(blank=False)
    def __str__(self):
        return f'{self.sensor}  {self.temp}'


