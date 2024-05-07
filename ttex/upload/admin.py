from django.contrib import admin
from .models import Transcription

# Register your models here.
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'user', 'status')

admin.site.register(Transcription, TranscriptionAdmin)
