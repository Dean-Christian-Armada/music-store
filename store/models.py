from __future__ import unicode_literals

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db import models

from django_elasticsearch.models import EsIndexable

# from core.methods import invalidate_cache




# Create your models here.
class Artist(EsIndexable, models.Model):
	name = models.CharField(max_length=50)
	birth_date = models.DateField()

	# https://docs.djangoproject.com/es/1.9/ref/models/instances/#get-absolute-url
	# Used to pass a location header URL upon post
	def get_absolute_url(self):
		return reverse('artists-detail', kwargs={'artist_id':self.id})

	def __unicode__(self):
		return self.name

	# def save(self, *args, **kwargs):
	# 	invalidate_cache(path=reverse('artists-list'))
	# 	super(Artist, self).save(*args, **kwargs)

# Example of post_save
def recache_artist(sender, **kwargs):
	cache.delete('artists')
# 	print "dean"
post_save.connect(recache_artist, sender=Artist)

class Album(EsIndexable, models.Model):
	artist = models.ForeignKey(Artist)
	name = models.CharField(max_length=50)
	description = models.TextField() 

	def get_absolute_url(self):
		return reverse('albums-detail', kwargs={'artist_id':self.artist.id, 'album_id':self.id})

	def __unicode__(self):
		return self.name

	def artist_details_dict(self):
		_id = self.artist.id
		name = self.artist.name
		birth_date = self.artist.birth_date
		return {"id":_id, "name":name, "birth_date": birth_date}

# Example of post_save
def recache_album(sender, **kwargs):
	cache.delete('albums')
# 	print "dean"
post_save.connect(recache_album, sender=Album)

class Song(EsIndexable, models.Model):
	album = models.ForeignKey(Album)
	name = models.CharField(max_length=50)
	duration = models.DurationField()
	ratings = models.IntegerField()

	def __unicode__(self):
		return self.name

	def album_details_dict(self):
		_id = self.album.id
		name = self.album.name
		desc = self.album.description
		artist_id = self.album.artist.id
		artist_name = self.album.artist.name
		artist_birth_date = self.album.artist.birth_date
		artist_details = {"id":artist_id, "name":artist_name, "birth_date":artist_birth_date}
		return {"id":_id, "name":name, "description": desc, "artist_id":artist_id, "artist_details":artist_details}