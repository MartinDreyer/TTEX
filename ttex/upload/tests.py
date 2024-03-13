from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from .models import Transcription
import os
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from .views import _save_audio_file
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from unittest.mock import patch

# Create your tests here.

class TranscriptionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a transcription object
        Transcription.objects.create(
            title='Test Transcription',
            user=user,
            status='PENDING',
            text='Lorem ipsum dolor sit amet'
        )

    def test_str_representation(self):
        transcription = Transcription.objects.get(id=1)
        self.assertEqual(str(transcription.text),'Lorem ipsum dolor sit amet')

    def test_default_title(self):
        transcription = Transcription.objects.get(id=1)
        self.assertEqual(transcription.title, 'Test Transcription')

    def test_created_at_auto_now_add(self):
        transcription = Transcription.objects.get(id=1)
        self.assertIsNotNone(transcription.created_at)

    def test_updated_at_auto_now(self):
        transcription = Transcription.objects.get(id=1)
        self.assertIsNotNone(transcription.updated_at)

    def test_user_foreign_key(self):
        transcription = Transcription.objects.get(id=1)
        self.assertIsInstance(transcription.user, User)

    def test_default_status(self):
        transcription = Transcription.objects.get(id=1)
        self.assertEqual(transcription.status, 'PENDING')




class SaveAudioFileTestCase(TestCase):
    def test_save_audio_file(self):
        # Create a mock request object with a dummy audio file
        audio_file = SimpleUploadedFile("audio.mp3", b"audio content")

        # Create a mock WSGI request object
        request = RequestFactory().post('/upload/', {'audio_file': audio_file})

        # Call the _save_audio_file function
        audio_file, file_path = _save_audio_file(request)

        # Assert that the audio file was saved correctly
        self.assertEqual(audio_file.name, 'audio.mp3')
        self.assertTrue(os.path.exists(file_path))

        # Clean up the temporary file
        os.remove(file_path)
        os.removedirs(os.path.dirname(file_path))

    
class SuccessViewTestCase(TestCase):
    def setUp(self):
        # Create a user for testing purposes
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.success_url = reverse('success')  # Make sure 'success' is the name of your URL pattern

    def test_redirect_if_not_logged_in(self):
        # Attempt to access the success view without being logged in
        response = self.client.get(self.success_url)
        # Check that the response is a redirect
        self.assertTrue(response.status_code, 302)
        # Check that the redirection URL is as expected (to the login page, for example)
        self.assertTrue(response.url.startswith('/'))

    def test_logged_in_uses_correct_template(self):
        # Log the user in
        self.client.login(username='testuser', password='12345')
        # Attempt to access the success view
        response = self.client.get(self.success_url)

        # Check that the user is logged in and the response code is 200
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'upload/success.html')




@override_settings(MEDIA_ROOT='/tmp/djangotest')
class StartBackgroundJobViewTest(TestCase):
    def setUp(self):
        # Create a user for testing purposes
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.start_job_url = reverse('transcribe')  # Adjust the name as necessary

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.start_job_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/'))

    def test_no_file_found_response(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.start_job_url, {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "No file found!")

    @patch('upload.views._save_audio_file')
    @patch('upload.views.transcribe.delay')
    def test_successful_file_upload_redirects(self, mock_transcribe, mock_save_audio_file):
        self.client.login(username='testuser', password='12345')

        # Mocking the file saving and async task
        mock_audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content")
        mock_save_audio_file.return_value = (mock_audio_file, "/fakepath/test_audio.mp3")
        
        # Make a request with the mocked file
        with self.settings(MEDIA_ROOT='/tmp'):
            response = self.client.post(self.start_job_url, {'audio_file': mock_audio_file}, format='multipart')

        # Verify the redirect
        self.assertRedirects(response, reverse('success'))  # Adjust the 'succes' to your success view's actual name
        # Ensure the transcribe.delay was called with expected arguments
        mock_transcribe.assert_called_once_with("/fakepath/test_audio.mp3", username='testuser')
