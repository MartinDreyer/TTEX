from django.db import models

# Create your models here.
class Transcription(models.Model):
    title = models.CharField(max_length=100, default='transcription', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='PENDING')
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    