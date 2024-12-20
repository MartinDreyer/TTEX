from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')

    def test_index_view_redirects_if_user_authenticated(self):
        # Create a logged-in user
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the index view
        response = self.client.get(self.url)

        # Assert that the response redirects to 'upload/' URL
        self.assertRedirects(response, reverse('upload'))

    def test_index_view_renders_template_if_user_not_authenticated(self):
        # Make a GET request to the index view
        response = self.client.get(self.url)

        # Assert that the response renders the 'core/index.html' template
        self.assertTemplateUsed(response, 'core/index.html')