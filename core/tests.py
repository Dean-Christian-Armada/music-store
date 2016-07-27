from django.test import TestCase

from rest_framework.test import APITestCase

# Create your tests here.

# url = ""
class OauthAccessToken(APITestCase):
	def setUp(self):
		print "dean"
		# self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)


class Dean(OauthAccessToken):
	def test_dean(self):
		pass