from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from unittest import skip # This library is used to skip some class TestCase

from store.models import Album

from . test_artists import ArtistRecordSetupMixing
 
import time # This library is used in case you want to put a sleep before proceeding to the next line of scripts
import inspect # This library is used to print the method of that certain class.. inspect.stack()[0][3]
import json # This library is for parsing the response.content

# Create your tests here.

url_1 = reverse('albums-list') # The URL endpoint for fetching all albums which is /albums/ having GET methods
url_2 = reverse('albums-filtered-by-artist',  kwargs={'artist_id':1}) # The URL endpoint for the albums of a certain artist which is /artists/:id/albums/ having POST and GET methods
url_3 = reverse('albums-detail', kwargs={'artist_id':1,'album_id':1}) # The URL endpoint for the albums which is /artists/:id/albums/:id having GET, PUT and DELETE methods
url_4 = reverse('albums-detail', kwargs={'artist_id':1,'album_id':3}) # Wrong id endpoint on purpose to check error response

# Reusabality Class
class AlbumRecordSetupMixing(ArtistRecordSetupMixing):
	# For reusable of adding a single record
	# To be used for POST, GET(detailed), PUT and DELETE
	def _setup_add_record(self):
		ArtistRecordSetupMixing._setup_add_record(self)
		_data = {"name": "Album 1", "description":"A Sample Album"}
		response = self.client.post(url_2, _data)
		data = json.loads(response.content)["data"]
		_data["artist"] = 1 # Appends a key-value in the json in response for the response of the serializer
		return ( response, _data, data )

_cls = AlbumRecordSetupMixing # Variable for the re-usable class

# Check the response if there is no given data
class AlbumTestWithData(APITestCase):
	# indent is just used to specify the tab size
	# follow the json naming format
	# Command: python manage.py dumpdata store.artist --indent=2 > store/fixtures/artists_2016_07_23.json
	# Command: python manage.py dumpdata store.album --indent=2 > store/fixtures/albums_2016_07_24.json
	fixtures = ['artists_2016_07_23.json', 'albums_2016_07_24.json']
	
	# Check the response if there is a data within
	def test_get(self):
		# self.client attribute will be an APIClient instance
		# Basically it will act as a client
		response = self.client.get(url_1)
		data = json.loads(response.content)["data"]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(len(data), 0) # There should be a data
		# print ("%s.%s DONE - 1" % (self.__class__.__name__, inspect.stack()[0][3]))

# Check the response if there is no given data
class AlbumTest(APITestCase, _cls):
	# Checks the records
	def test_get(self):
		# self.client attribute will be an APIClient instance
		# Basically it will act as a client
		response = self.client.get(url_1)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(response.content, '') # There should be no data
		# self.assertEqual(len(data), 0)
		# print ("%s.%s DONE - 1" % (self.__class__.__name__, inspect.stack()[0][3]))

	# Creates the record
	def test_post(self):
		x = _cls._setup_add_record(self)
		self.assertEqual(x[0].status_code, status.HTTP_201_CREATED) # Status 201 is the default when a new object is created
		self.assertIn("artist_detail", x[2]) # Just make sure that a certain key is included
		# self.assertIn("Dean", "Dean Armada") # have the API return the updated (or created) representation as part of the response
		self.assertEqual(Album.objects.count(), 1) # Make  sure that there is a craeted instance
		self.assertEqual(Album.objects.get().name, 'Album 1') # Double checking if the last post is the created instance
		self.assertEqual(x[0]["Location"], Album.objects.get().get_absolute_url())

	# Get a specific record
	def test_get_detail(self):
		x = _cls._setup_add_record(self)
		response = self.client.get(url_2)
		data = json.loads(response.content)["data"]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# self.assertEqual(data, x[1])
		self.assertNotEqual(len(data), 0)

	# # Update a specific record
	def test_put(self):
		x = _cls._setup_add_record(self)
		# Check if updating without the artist key-value pair will just change the name and description 
		update = {"name": "Album 5", "description":"A Sample Album 5"}
		response = self.client.put(url_3, update)
		data = json.loads(response.content)["data"]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(Album.objects.get().name, 'Album 1') # Check if it is still the old name
		self.assertEqual(Album.objects.get().name, 'Album 5') # Check the new name
		y = _cls._setup_add_record(self)
		# Check if updating with the artist key-value pair will change the artist as well
		update_2 = {"name": "Album 6", "description":"A Sample Album 6", "artist": 2}
		response = self.client.put(url_3, update_2)
		data = json.loads(response.content)["data"]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(Album.objects.filter()[0].name, 'Album 5') # Check if it is still the old name
		self.assertEqual(Album.objects.filter()[0].name, 'Album 6') # Check the new name
		self.assertEqual(Album.objects.filter()[0].artist.id, 2) # Check the new artist

	def test_delete(self):
		x = _cls._setup_add_record(self)
		response = self.client.delete(url_3)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		response = self.client.get(url_3)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# Check the response if there is error on requests
class AlbumTestErrors(_cls, APITestCase):
	# User tries to request a POST method without a "name"
	def test_post(self):
		_data = {"description":"A Sample Album 6"}
		response = self.client.post(url_2, _data)
		data = json.loads(response.content)["errors"] # checks the errors
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotEqual(len(data), 0)

	# User tries to request a GET method on a non-existing id
	def test_get_detail(self):
		x = _cls._setup_add_record(self)
		response = self.client.get(url_4)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	# User tries to request a PUT method without a "name"
	def test_put(self):
		x = _cls._setup_add_record(self)
		update = {"description":"A Sample Album 6"}
		response = self.client.put(url_3, update)
		data = json.loads(response.content)["errors"]
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotEqual(len(data), 0)

	# User tries to request a DELETE method on a non-existing id
	def test_delete(self):
		x = _cls._setup_add_record(self)
		response = self.client.delete(url_4)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)