from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.methods import standardResponse

from api.v1.store.serializers import *

from store.models import *

class AlbumsList(APIView):
	"""
	**GET** - lists all Albums
	"""
	serializer_class = AlbumSerializer

	def get(self, request, *args, **kwargs):
		page = request.GET.get('page', None)
		_array = Album.objects.filter()
		if page:
			x = pagination(page)
			_array = _array[x[0]:x[1]]
		serializer = self.serializer_class(_array, many=True)
		if serializer.data:
			_status = status.HTTP_200_OK
		else:
			_status = status.HTTP_204_NO_CONTENT
		return Response(standardResponse(data=serializer.data), status=_status)
album = AlbumsList.as_view()

class AlbumsFilteredByArtist(APIView):
	"""
**GET** - lists all the Albums of an Artist

**POST** - creates a new record
	"""
	serializer_class = AlbumSerializer # serializer_class is important to automatically show fields on DRF docs

	def get(self, request, *args, **kwargs):
		id_1 = kwargs['artist_id']
		_array = Album.objects.filter(artist_id=id_1)
		serializer = self.serializer_class(_array, many=True)
		if serializer.data:
			_status = status.HTTP_200_OK
		else:
			_status = status.HTTP_204_NO_CONTENT
		return Response(standardResponse(data=serializer.data), status=_status)

	def post(self, request, *args, **kwargs):
		id_1 = kwargs['artist_id']
		request.data["artist"] = id_1 # Adds the artist key-value based on URL
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			obj = serializer.save()
			response = Response(standardResponse(data=serializer.data), status=status.HTTP_201_CREATED)
			response['Location'] = obj.get_absolute_url()
			return response
		else:
			return Response(standardResponse(errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)
afba = AlbumsFilteredByArtist.as_view()

class AlbumsDetail(APIView):
	"""
**GET** - gets a specific artist

**PUT** - updates an artist

**DELETES** - deletes an artist
	"""
	serializer_class = AlbumSerializer
	obj = Album # This is needed as model parameters does not work smoothly on the get_obj custom method
	parent_obj = Artist

	def get_obj(self, id_1, id_2):
		try:
			_obj = self.obj.objects.get(artist_id=id_1, pk=id_2)
			return _obj
		except:
			return 0


	def get(self, request, *args, **kwargs):
		# kwargs is used to get the parameters
		id_1 = kwargs['artist_id']
		id_2 = kwargs['album_id']
		obj = self.get_obj(id_1, id_2)
		if obj:
			serializer = self.serializer_class(obj)
			return Response(standardResponse(data=serializer.data), status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)

	def put(self, request, *args, **kwargs):
		id_1 = kwargs['artist_id']
		id_2 = kwargs['album_id']
		try: # If artist is visible in the request then the artist will be replaced
			request.data["artist"]
		except: # If there is no artist then the artist_id param in the URL will be used and the artist will remain the same
			request.data["artist"] = id_1
		obj = self.get_obj(id_1, id_2)
		if obj:
			serializer = self.serializer_class(obj, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(standardResponse(data=serializer.data), status=status.HTTP_200_OK)
			else:
				# return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
				return Response(standardResponse(errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, *args, **kwargs):
		id_1 = kwargs['artist_id']
		id_2 = kwargs['album_id']
		obj = self.get_obj(id_1, id_2)
		if obj:
			serializer = self.serializer_class(obj)
			obj.delete()
			return Response(standardResponse(data=serializer.data), status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
album_detail = AlbumsDetail.as_view()