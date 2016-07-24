from django.conf.urls import url, include

urlpatterns = [
	# url(r'^artists/', include('api.v1.store.artists.urls'), name="dean"),
 	url(r'^', include('api.v1.store.urls')),
 	url(r'^docs/', include('rest_framework_docs.urls')),
]