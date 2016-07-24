from __future__ import unicode_literals

from django.db import models

# Create your models here.
class StoreDashBoard(models.Model):
	artist = models.CharField(max_length=50)
	album = models.CharField(max_length=50)
	song = models.CharField(max_length=50)
	duration = models.DurationField()
	ratings = models.IntegerField()