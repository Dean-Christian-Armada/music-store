# from django.shortcuts import render

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from music_store.settings import standardResponse

# from api.v1.store.serializers import *

# from . models import *

# # Create your views here.

# class ArtistsList(APIView):
# 	"""
# **GET** - lists all the artists

# **POST** - creates a new record
# 	"""
# 	serializer_class = ArtistSerializer # serializer_class is important to automatically show fields on DRF docs

# 	def get(self, request, *args, **kwargs):
# 		_array = Artist.objects.filter()
# 		serializer = self.serializer_class(_array, many=True)
# 		if serializer.data:
# 			_status = status.HTTP_200_OK
# 		else:
# 			_status = status.HTTP_204_NO_CONTENT
# 		return Response(standardResponse(data=serializer.data), status=_status)

# 	def post(self, request, *args, **kwargs):
# 		serializer = self.serializer_class(data=request.data)
# 		if serializer.is_valid():
# 			obj = serializer.save()
# 			response = Response(standardResponse(data=serializer.data), status=status.HTTP_201_CREATED)
# 			response['Location'] = obj.get_absolute_url()
# 			return response
# 		else:
# 			return Response(standardResponse(errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)
# artist = ArtistsList.as_view()

# class ArtistsDetail(APIView):
# 	"""
# **GET** - gets a specific artist

# **PUT** - updates an artist

# **DELETES** - deletes an artist
# 	"""
# 	serializer_class = ArtistSerializer
# 	obj = Artist # This is needed as model parameters does not work smoothly on the get_obj custom method

# 	def get_obj(self, id):
# 		try:
# 			_obj = self.obj.objects.get(pk=id)
# 			return _obj
# 		except:
# 			return 0


# 	def get(self, request, *args, **kwargs):
# 		# kwargs is used to get the parameters
# 		_id = kwargs['artist_id']
# 		obj = self.get_obj(_id)
# 		if obj:
# 			serializer = self.serializer_class(obj)
# 			return Response(standardResponse(data=serializer.data), status=status.HTTP_200_OK)
# 		else:
# 			return Response(status=status.HTTP_404_NOT_FOUND)

# 	def put(self, request, *args, **kwargs):
# 		_id = kwargs['artist_id']
# 		obj = self.get_obj(_id)
# 		if obj:
# 			serializer = self.serializer_class(obj, data=request.data)
# 			if serializer.is_valid():
# 				serializer.save()
# 				return Response(standardResponse(data=serializer.data), status=status.HTTP_200_OK)
# 			else:
# 				# return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
# 				return Response(standardResponse(errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)

# 	def delete(self, request, *args, **kwargs):
# 		_id = kwargs['artist_id']
# 		obj = self.get_obj(_id)
# 		if obj:
# 			serializer = self.serializer_class(obj)
# 			obj.delete()
# 			return Response(standardResponse(data=serializer.data), status=status.HTTP_200_OK)
# 		else:
# 			return Response(status=status.HTTP_400_BAD_REQUEST)
# artist_detail = ArtistsDetail.as_view()

# class AlbumsList(APIView):
# 	"""
# **GET** - lists all the Albums

# **POST** - creates a new record
# 	"""
# 	serializer_class = AlbumSerializer # serializer_class is important to automatically show fields on DRF docs

# 	def get(self, request, *args, **kwargs):
# 		_array = Album.objects.filter()
# 		serializer = self.serializer_class(_array, many=True)
# 		if serializer.data:
# 			_status = status.HTTP_200_OK
# 		else:
# 			_status = status.HTTP_204_NO_CONTENT
# 		return Response(standardResponse(data=serializer.data), status=_status)

# 	def post(self, request, *args, **kwargs):
# 		serializer = self.serializer_class(data=request.data)
# 		if serializer.is_valid():
# 			obj = serializer.save()
# 			response = Response(standardResponse(data=serializer.data), status=status.HTTP_201_CREATED)
# 			response['Location'] = obj.get_absolute_url()
# 			return response
# 		else:
# 			return Response(standardResponse(errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)
# album = AlbumsList.as_view()


# @api_view(['GET','POST'])
# def album(request, artist_id):
# 	pass

# @api_view(['GET','PATCH','DELETE'])
# def album_detail(request, artist_id, album_id):
# 	pass

# @api_view(['GET','POST'])
# def song(request, artist_id, album_id):
# 	pass

# @api_view(['GET','PATCH','DELETE'])
# def song_detail(request, artist_id, album_id, song_id):
# 	pass