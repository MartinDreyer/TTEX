from upload.models import Transcription
from django import forms


class TranscriptionForm(forms.ModelForm):
    class Meta:
        model = Transcription
        fields = ('title', 'text',)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance