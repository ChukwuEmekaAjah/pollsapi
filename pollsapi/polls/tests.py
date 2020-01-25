from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from polls import apiviews

# Create your tests here.

class TestPoll(APITestCase):
	def setUp(self):
		self.factory = APIRequestFactory()
		self.view = apiviews.PollList.as_view()
		self.uri = '/api/polls'
		self.user = self.setup_user()
		self.token = Token.objects.create(user=self.user)
		self.token.save()
		self.client = APIClient()

	@staticmethod
	def setup_user():
		User = get_user_model()
		return User.objects.create_user(
			'test', email='test@m.com', password='test'
		)

	def test_list(self):
		request = self.factory.get(self.uri, HTTP_AUTHORIZATION='Toke {}'.format(self.token.key))
		request.user = self.user 
		response = self.view(request)
		self.assertEqual(response.status_code, 200, 'Expected Response code 200, received {0} instead'.format(response.status_code))


	def test_list2(self):
		self.client.login(username='test', password='test')
		response = self.client.get(self.uri)
		self.assertEqual(response.status_code, 200, 'Expected Response code 200, received {0} instead'.format(response.status_code))

	def test_create(self):
		self.client.login(username='test', password='test')
		params = {
			"question":"What is my name",
			"create_by":1
		}
		response = self.client.post(self.uri, params)
		self.assertEqual(response.status_code, 201, "Expected response code: 201 but got {}".format(response.status_code))
