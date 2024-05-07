from django.db import models
import uuid


# Create your models here.
class Transcription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=100, default='transcription')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='PENDING')
    text = models.TextField(null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"http://localhost:8000/transcriptions/{self.id}"
