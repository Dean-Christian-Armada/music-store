from rest_framework import serializers

from store.models import *

class ArtistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Artist
		fields = ('name', 'birth_date')

class AlbumSerializer(serializers.ModelSerializer):
	artist_detail = serializers.SerializerMethodField()

	def get_artist_detail(self, obj):
		x = obj.artist.id
		item = Artist.objects.get(id=x)
		serializer = ArtistSerializer(item)
		serializer = dict(serializer.data) # Converted to dictionary to add more key-value
		serializer["id"] = x
		return serializer

	class Meta:
		model = Album
		fields = ('artist', 'name', 'description', 'artist_detail')

class SongSerializer(serializers.ModelSerializer):
	class Meta:
		model = Song
		fields = ('album', 'name', 'duration', 'ratings')