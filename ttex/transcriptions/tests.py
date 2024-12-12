from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from upload.models import Transcription
import uuid

class TranscriptionsViewTest(TestCase):
    def setUp(self):
        self.testid = uuid.uuid4()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.transcription = Transcription.objects.create(title='Test Transcription', text='Test Content', user=self.user, id=self.testid)

    def test_index_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('transcriptions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Transcription')
        self.assertTemplateUsed(response, 'transcriptions/index.html')

    def test_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('detail', args=[self.transcription.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Transcription')
        self.assertContains(response, 'Test Content')
        self.assertTemplateUsed(response, 'transcriptions/detail.html')
    
    def test_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_transcription', args=[self.transcription.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transcriptions/transcription_deleted.html')
        self.assertFalse(Transcription.objects.filter(id=self.transcription.id).exists())

    def test_edit_view_with_valid_form(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('edit', args=[self.transcription.id])
        response = self.client.post(url, {'title': 'Updated Title'})
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect
        self.assertEqual(response.url, reverse('detail', args=[self.transcription.id]))  # Check if the redirect URL is correct
        updated_transcription = Transcription.objects.get(id=self.transcription.id)
        self.assertEqual(updated_transcription.title, 'Updated Title')  # Check if the title is updated
