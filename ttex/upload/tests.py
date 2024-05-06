from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Transcription
import uuid
class TranscriptionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a transcription object
        transcription_id = uuid.uuid4()
        Transcription.objects.create(
            id=transcription_id,
            title='Test Transcription',
            user=user,
            status='PENDING',
            text='Lorem ipsum dolor sit amet',
        )

    def test_str_representation(self):
        transcription = Transcription.objects.first()
        self.assertEqual(str(transcription), 'Test Transcription')

    def test_absolute_url(self):
        transcription = Transcription.objects.first()
        expected_url = f'http://localhost:8000/transcriptions/{transcription.id}'
        self.assertEqual(transcription.get_absolute_url(), expected_url)

class UploadViewTest(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.login_url = reverse('index')  
        self.upload_url = reverse('upload')  # Replace 'upload' with the actual name of your upload view in urls.py

    def test_redirect_if_not_logged_in(self):
        # Attempt to access the upload page without being logged in
        response = self.client.get(self.upload_url, follow=True)
        # Check if the response redirects to the login page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertTrue(response.redirect_chain)
        final_url = response.redirect_chain[-1][0]  # Get final URL from the redirect chain
        expected_url = '/'  
        self.assertEqual(final_url, expected_url)

        

    def test_logged_in_uses_correct_template(self):
        # Log in the user
        self.client.login(username='testuser', password='12345')
        # Attempt to access the upload page
        response = self.client.get(self.upload_url)
        # Check that the user is logged in and the correct template is used
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload/upload.html')

class SuccessViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_success_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload/success.html')
