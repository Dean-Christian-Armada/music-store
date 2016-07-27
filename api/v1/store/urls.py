from django.conf.urls import url, include

from store.views.v1 import views_artists as va
from store.views.v1 import views_albums as va_2

urlpatterns = [
	# START Artists URLS
 	url(r'^artists/$', va.artist, name='artists-list'),
 	url(r'^artists/(?P<artist_id>[0-9]+)/$', va.artist_detail, name='artists-detail'),
 	# END Artists URLS
 	# START Album URLS
 	url(r'^albums/$', va_2.album, name='albums-list'),
 	url(r'^artists/(?P<artist_id>[0-9]+)/albums/$', va_2.afba, name='albums-filtered-by-artist'),
 	url(r'^artists/(?P<artist_id>[0-9]+)/albums/(?P<album_id>[0-9]+)', va_2.album_detail, name='albums-detail'),
 	# END Album URLS
 	# START Song URLS
 	# url(r'^artists/(?P<artist_id>[0-9]+)/albums/(?P<album_id>[0-9]+)/songs/', views.song, name='songs'),
 	# url(r'^artists/(?P<artist_id>[0-9]+)/albums/(?P<album_id>[0-9]+)/songs/(?P<song_id>[0-9]+)/', views.song_detail, name='songs-detail'),
 	# END Song URLS
]