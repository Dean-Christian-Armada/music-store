from django.conf.urls import url, include

from store.views import views_artists as va
from store.views import views_albums as va_2

urlpatterns = [
 	url(r'^artists/$', va.artist, name='artists-list'),
 	url(r'^artists/(?P<artist_id>[0-9]+)/$', va.artist_detail, name='artists-detail'),
 	url(r'^artists/(?P<artist_id>[0-9]+)/albums/$', va_2.album, name='albums'),
 	# url(r'^artists/(?P<artist_id>[0-9]+)/albums/(?P<album_id>[0-9]+)', views.album_detail, name='albums-detail'),
 	# url(r'^artists/(?P<artist_id>[0-9]+)/albums/(?P<album_id>[0-9]+)/songs/', views.song, name='songs'),
 	# url(r'^artists/(?P<artist_id>[0-9]+)/albums/(?P<album_id>[0-9]+)/songs/(?P<song_id>[0-9]+)/', views.song_detail, name='songs-detail'),
]