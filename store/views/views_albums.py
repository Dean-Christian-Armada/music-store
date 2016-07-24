from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from music_store.settings import standardResponse

from api.v1.store.serializers import *

from store.models import *

class AlbumsList(APIView):
	"""
**GET** - lists all the Albums

**POST** - creates a new record
	"""
	serializer_class = AlbumSerializer # serializer_class is important to automatically show fields on DRF docs

	def get(self, request, *args, **kwargs):
		_array = Album.objects.filter()
		serializer = self.serializer_class(_array, many=True)
		if serializer.data:
			_status = status.HTTP_200_OK
		else:
			_status = status.HTTP_204_NO_CONTENT
		return Response(standardResponse(data=serializer.data), status=_status)

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			obj = serializer.save()
			response = Response(standardResponse(data=serializer.data), status=status.HTTP_201_CREATED)
			response['Location'] = obj.get_absolute_url()
			return response
		else:
			return Response(standardResponse(errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)
album = AlbumsList.as_view()