# from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.core.signals import request_started, request_finished
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.methods import standardResponse, pagination, request_to_kwargs
from core.classes import CacheMixin

from api.v1.store.serializers import *

from store.models import *

import time

class SongsList(APIView):
	"""
**GET** - lists all the songs

**POST** - creates a new record
	"""
	serializer_class = SongSerializer # serializer_class is important to automatically show fields on DRF docs

	def get(self, request, *args, **kwargs):

		page = request.GET.get('page', None)
		sort = request.GET.get('sort', None)
		filters = dict(request.GET.copy()) # Used for filtering the ORM
		_array = Song.objects.filter()
		if sort:
			del filters["sort"]
			sort = sort.split(',')
			_array = _array.order_by(*sort)
		if page:
			del filters["page"]
			x = pagination(page)
		if filters:
			_array = _array.filter(**request_to_kwargs(filters))
		try:
			_array = _array[x[0]:x[1]]
		except:
			pass
		# print _array.values('name', 'album__name')
		serializer = self.serializer_class(_array, many=True)
		data = serializer.data
		if data:
			_status = status.HTTP_200_OK
		else:
			_status = status.HTTP_204_NO_CONTENT
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
song = SongsList.as_view()