from django.conf.urls import url, include

from store import views

urlpatterns = [
 	url(r'^artists/$', views.artist, name='artists-list'),
 	url(r'^artists/(?P<artist_id>[0-9]+)/$', views.artist_detail, name='artists-detail'),
 	url(r'^artists/(?P<artist_id>[0-9]+)/albums/$', views.album, name='albums'),
 	# url(r'^artists/(?P<artist_id>[0-9]+)/albums/(?P<album_id>[0-9]+)', views.album_detail, name='albums-detail'),
 	# url(r'^artists/(?P<artist_id>[0-9]+)/albums/(?P<album_id>[0-9]+)/songs/', views.song, name='songs'),
 	# url(r'^artists/(?P<artist_id>[0-9]+)/albums/(?P<album_id>[0-9]+)/songs/(?P<song_id>[0-9]+)/', views.song_detail, name='songs-detail'),
]