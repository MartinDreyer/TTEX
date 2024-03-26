from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from upload.models import Transcription

class TranscriptionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.transcription = Transcription.objects.create(title='Test Transcription', text='Test Content', user=self.user)

    def test_edit_view_with_valid_form(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('edit', args=[self.transcription.id])
        response = self.client.post(url, {'title': 'Updated Title', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect
        self.assertEqual(response.url, reverse('detail', args=[self.transcription.id]))  # Check if the redirect URL is correct
        updated_transcription = Transcription.objects.get(id=self.transcription.id)
        self.assertEqual(updated_transcription.title, 'Updated Title')  # Check if the title is updated
        self.assertEqual(updated_transcription.content, 'Updated Content')  # Check if the content is updated

    def test_edit_view_with_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('edit', args=[self.transcription.id])
        response = self.client.post(url, {'title': '', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 200)  # Check if the response is a success
        form = response.context['form']
        self.assertFalse(form.is_valid())  # Check if the form is invalid
        self.assertContains(response, 'This field is required.')  # Check if the error message is displayed

    def test_edit_view_with_unauthenticated_user(self):
        url = reverse('edit', args=[self.transcription.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect
        self.assertEqual(response.url, '/accounts/login/?next=' + url)  # Check if the redirect URL is correct

    def test_edit_view_with_nonexistent_transcription(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('edit', args=[9999])  # Nonexistent transcription ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Check if the response is a not found

    def test_edit_view_with_get_request(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('edit', args=[self.transcription.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Check if the response is a success
        form = response.context['form']
        self.assertTrue(form.instance == self.transcription)  # Check if the form instance is correct