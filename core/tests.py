from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

import ast

# Create your tests here.

url = "http://127.0.0.1:8000/o/token/"
url_1 = reverse('artists-list')

class OauthAccessToken(APITestCase):

	# python manage.py dumpdata oauth2_provider.application --indent=2 > core/fixtures/applications_2016_07_27.json
	# python manage.py dumpdata auth.User --indent=2 > core/fixtures/users_2016_07_27.json
	# users is required because it is a foreign key of the applications
	fixtures = ['users_2016_07_27.json', 'applications_2016_07_27.json']
	# fixtures = ['users_2016_07_27.json', 'applications_2016_07_27.json', 'artists_2016_07_23.json']

	def setUp(self):
		_data = "Basic a1JBc0pZaVhHc05yeFFsZ1JQcEtuOTVvUVFsV1ZwZXMxczh6bWp1WTp1ZGlHcGtodHNwaWljWjNRM3ZmR05SZ0RwdHhsMDFJR2prSU5RemdDQm9FbGttbUx2VDZUM29pMkhlUVI5T1dXbG0yMHJnak45V1FPR081c3Jla3p0WHc2eFo1SjB3V3phTWJJQWNJMWlUYlFsU2M3cWtiRktJdU9XNDdVVWdVWg=="
		token = "Basic a1JBc0pZaVhHc05yeFFsZ1JQcEtuOTVvUVFsV1ZwZXMxczh6bWp1WTp1ZGlHcGtodHNwaWljWjNRM3ZmR05SZ0RwdHhsMDFJR2prSU5RemdDQm9FbGttbUx2VDZUM29pMkhlUVI5T1dXbG0yMHJnak45V1FPR081c3Jla3p0WHc2eFo1SjB3V3phTWJJQWNJMWlUYlFsU2M3cWtiRktJdU9XNDdVVWdVWg=="
		_data = "grant_type=password&username=dean&password=armadaarmada"
		self.client.credentials(HTTP_AUTHORIZATION=token)
		response = self.client.post(url, _data, content_type="application/x-www-form-urlencoded")
		response = response.content # Gets the content of the response
		response = ast.literal_eval(response) # Converts the json to dictionary
		_token = response["access_token"] # this will be the authorization with the access token 
		auth = "Bearer "+_token # The Authorization Header of Oauth
		self.client.credentials(HTTP_AUTHORIZATION=auth)

# class Dean(OauthAccessToken):
# 	def test_dean(self):
# 		auth = self.setUp()
# 		self.client.credentials(HTTP_AUTHORIZATION=auth)
# 		response = self.client.get(url_1)