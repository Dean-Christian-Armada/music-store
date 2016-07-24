from rest_framework import serializers

from store.models import *

class ArtistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Artist
		fields = ('name', 'birth_date')

class AlbumSerializer(serializers.ModelSerializer):
	class Meta:
		model = Album
		fields = ('artist', 'name', 'description')

class SongSerializer(serializers.ModelSerializer):
	class Meta:
		model = Song
		fields = ('album', 'name', 'duration', 'ratings')