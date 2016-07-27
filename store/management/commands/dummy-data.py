# Source: https://qbox.io/blog/elasticsearch-python-django-database
from django.core.management.base import BaseCommand

from model_mommy import mommy

from store.models import *

class Command(BaseCommand):
	help = "My command for filling up my store"
	def add_arguments(self, parser):
		parser.add_argument('count', nargs=1, type=int)
	def handle(self, *args, **options):
		self.make_artists()
		self.make_albums(options)
	# def make_artists(self, options):
	def make_artists(self):
		import radar
		import datetime

		# Generate random datetime from datetime.datetime values
		radar.random_datetime(
		    start = datetime.datetime(year=1980, month=1, day=1),
		    stop = datetime.datetime(year=2000, month=1, day=1)
		)
		_artists = ("Justin Bieber", "Anne Curtis", "Eminem", "Tupac", "Loonie")
		self.artists = []
		for name in _artists:
			# print options.get('count')[0]
			uni = mommy.make(Artist, name=name, birth_date=radar.random_datetime())
			self.artists.append(uni)

	def make_albums(self, options):
		import names
		import random
		self.albums = []
		for x in range(0, options.get('count')[0]):
			album = mommy.prepare(
				Album,
				artist=random.choice(self.artists),
				name=names.get_first_name(),
				description="Sample Description",
			)
			self.albums.append(album)
		Album.objects.bulk_create(self.albums)