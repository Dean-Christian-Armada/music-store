from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
class Artist(models.Model):
	name = models.CharField(max_length=50)
	birth_date = models.DateField()

	# https://docs.djangoproject.com/es/1.9/ref/models/instances/#get-absolute-url
	# Used to pass a location header URL upon post
	def get_absolute_url(self):
		return reverse('artists-detail', kwargs={'artist_id':self.id})

class Album(models.Model):
	artist = models.ForeignKey(Artist)
	name = models.CharField(max_length=50)
	description = models.TextField() 

class Song(models.Model):
	album = models.ForeignKey(Album)
	name = models.CharField(max_length=50)
	duration = models.DurationField()
	ratings = models.IntegerField()