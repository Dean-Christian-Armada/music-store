from rest_framework import serializers

from store.models import *

class ArtistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Artist
		fields = ('name', 'birth_date')

class AlbumSerializer(serializers.ModelSerializer):
	# This is a lot faster than using the SerializerMethodField
	artist_detail = serializers.DictField(source="artist_details_dict", read_only=True)
	# artist_detail = serializers.SerializerMethodField()

	# Was used when using serializerMethodField
	# def get_artist_detail(self, obj):
	# 	x = obj.artist.id
	# 	item = Artist.objects.get(id=x)
	# 	serializer = ArtistSerializer(item)
	# 	serializer = dict(serializer.data) # Converted to dictionary to add more key-value
	# 	# serializer["id"] = x
	# 	return serializer

	class Meta:
		model = Album
		fields = ('artist', 'name', 'description', 'artist_detail')

class SongSerializer(serializers.ModelSerializer):
	album_detail = serializers.DictField(source="album_details_dict", read_only=True)

	class Meta:
		model = Song
		fields = ('name', 'duration', 'ratings', 'album_detail')