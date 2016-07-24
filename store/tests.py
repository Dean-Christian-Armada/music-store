from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from unittest import skip # This library is used to skip some class TestCase

from . models import *
 
import time # This library is used in case you want to put a sleep before proceeding to the next line of scripts
import inspect # This library is used to print the method of that certain class.. inspect.stack()[0][3]
import json # This library is for parsing the response.content

# Create your tests here.

url_1 = reverse('artists-list') # The URL endpoint for the artists which is /artists/ having POST and GET methods
url_2 = reverse('artists-detail', kwargs={'artist_id':1}) # The URL endpoint for the artists which is /artists/:d having GET, PUT and DELETE methods
url_3 = reverse('artists-detail', kwargs={'artist_id':3}) # Wrong id endpoint on purpose to check error response

# Reusabality Class
class ArtistRecordSetupMixing():
	# For reusable of adding a single record
	# To be used for POST, GET(detailed), PUT and DELETE
	def _setup_add_record(self):
		_data = {"name": "50 Cent", "birth_date":"2005-02-13"}
		response = self.client.post(url_1, _data)
		data = json.loads(response.content)["data"]
		return ( response, _data, data )

_cls = ArtistRecordSetupMixing # Variable for the re-usable class

# Check the response if there is no given data
class ArtistTestWithData(APITestCase):
	# indent is just used to specify the tab size
	# follow the json naming format
	# Command: python manage.py dumpdata store.artist --indent=2 > store/fixtures/artists_2016_07_23.json
	fixtures = ['artists_2016_07_23.json']
	
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
class ArtistTest(APITestCase, _cls):
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
		self.assertEqual(x[2], x[1]) # have the API return the updated (or created) representation as part of the response
		self.assertEqual(Artist.objects.count(), 1) # Make  sure that there is a craeted instance
		self.assertEqual(Artist.objects.get().name, '50 Cent') # Double checking if the last post is the created instance

	# Get a specific record
	def test_get_detail(self):
		x = _cls._setup_add_record(self)
		response = self.client.get(url_2)
		data = json.loads(response.content)["data"]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(data, x[1])
		self.assertNotEqual(len(data), 0)

	# Update a specific record
	def test_put(self):
		x = _cls._setup_add_record(self)
		update = {"name": "60 Cents", "birth_date":"2005-02-13"}
		response = self.client.put(url_2, update)
		data = json.loads(response.content)["data"]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(data, x[1])
		self.assertNotEqual(Artist.objects.get().name, '50 Cent') # Check if it is still the old name
		self.assertEqual(Artist.objects.get().name, '60 Cents') # Check the new name

	def test_delete(self):
		x = _cls._setup_add_record(self)
		response = self.client.delete(url_2)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		response = self.client.get(url_2)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# Check the response if there is error on requests
class ArtistTestErrors(_cls, APITestCase):
	# User tries to request a POST method without a "name"
	def test_post(self):
		_data = {"birth_date":"2005-02-13"}
		response = self.client.post(url_1, _data)
		data = json.loads(response.content)["errors"] # checks the errors
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotEqual(len(data), 0)

	# User tries to request a GET method on a non-existing id
	def test_get_detail(self):
		_cls._setup_add_record(self)
		response = self.client.get(url_3)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	# User tries to request a PUT method without a "name"
	def test_put(self):
		x = _cls._setup_add_record(self)
		update = {"birth_date":"2005-02-13"}
		response = self.client.put(url_2, update)
		data = json.loads(response.content)["errors"]
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotEqual(len(data), 0)

	# User tries to request a DELETE method on a non-existing id
	def test_delete(self):
		x = _cls._setup_add_record(self)
		response = self.client.delete(url_3)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


