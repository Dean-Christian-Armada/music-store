from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.core.signals import request_started, request_finished
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.methods import standardResponse, pagination
from core.classes import CacheMixin

from api.v1.store.serializers import *

from store.models import *

import time

# Create your views here.
# An Example of Measuring the requests speed
# @cache_page(60 * 1)
class ArtistsList(APIView):
	"""
**GET** - lists all the artists

**POST** - creates a new record
	"""
	serializer_class = ArtistSerializer # serializer_class is important to automatically show fields on DRF docs

	def get(self, request, *args, **kwargs):
		# global serializer_time
		# global db_time

		page = request.GET.get('page', None)
		# db_start = time.time()
		c = 'artists'
		if cache.get(c):
			_array = cache.get(c)
		else:
			_array = Artist.objects.filter()
			cache.set(c, _array)
		# db_time = time.time() - db_start
		if page:
			x = pagination(page)
			_array = _array[x[0]:x[1]]
		# serializer_start = time.time()
		serializer = self.serializer_class(_array, many=True)
		data = serializer.data
		if data:
			_status = status.HTTP_200_OK
		else:
			_status = status.HTTP_204_NO_CONTENT
		# serializer_time = time.time() - serializer_start
		return Response(standardResponse(data=data), status=_status)

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			obj = serializer.save()
			response = Response(standardResponse(data=serializer.data), status=status.HTTP_201_CREATED)
			response['Location'] = obj.get_absolute_url()
			return response
		else:
			return Response(standardResponse(errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)

	# THESE ARE CONFLICTED WHEN RUNNING AUTOMATION TESTS
	# def dispatch(self, request, *args, **kwargs):
	# 	global dispatch_time
	# 	global render_time

	# 	dispatch_start = time.time()
	# 	ret = super(ArtistsList, self).dispatch(request, *args, **kwargs)

	# 	render_start = time.time()
	# 	ret.render()
	# 	render_time = time.time() - render_start

	# 	dispatch_time = time.time() - dispatch_start

	# 	return ret

	# def started(sender, **kwargs):
	# 	global started
	# 	started = time.time()

	# def finished(sender, **kwargs):
	# 	total = time.time() - started
	# 	api_view_time = dispatch_time - (render_time + serializer_time + db_time)
	# 	request_response_time = total - dispatch_time

	# 	print ("Database lookup               | %.4fs" % db_time)
	# 	print ("Serialization                 | %.4fs" % serializer_time)
	# 	print ("Django request/response       | %.4fs" % request_response_time)
	# 	print ("API view                      | %.4fs" % api_view_time)
	# 	print ("Response rendering            | %.4fs" % render_time)

	# request_started.connect(started)
	# request_finished.connect(finished)

artist = ArtistsList.as_view()

class ArtistsDetail(APIView):
	"""
**GET** - gets a specific artist

**PUT** - updates an artist

**DELETES** - deletes an artist
	"""
	serializer_class = ArtistSerializer
	obj = Artist # This is needed as model parameters does not work smoothly on the get_obj custom method

	def get_obj(self, id):
		try:
			_obj = self.obj.objects.get(pk=id)
			return _obj
		except:
			return 0


	def get(self, request, *args, **kwargs):
		# kwargs is used to get the parameters
		_id = kwargs['artist_id']
		obj = self.get_obj(_id)
		if obj:
			serializer = self.serializer_class(obj)
			return Response(standardResponse(data=serializer.data), status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)

	def put(self, request, *args, **kwargs):
		_id = kwargs['artist_id']
		obj = self.get_obj(_id)
		if obj:
			serializer = self.serializer_class(obj, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(standardResponse(data=serializer.data), status=status.HTTP_200_OK)
			else:
				# return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
				return Response(standardResponse(errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, *args, **kwargs):
		_id = kwargs['artist_id']
		obj = self.get_obj(_id)
		if obj:
			serializer = self.serializer_class(obj)
			obj.delete()
			return Response(standardResponse(data=serializer.data), status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
artist_detail = ArtistsDetail.as_view()
