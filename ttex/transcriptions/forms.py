from upload.models import Transcription
from django import forms


class TranscriptionForm(forms.ModelForm):
    class Meta:
        model = Transcription
        fields = ('title', 'text',)

    def __init__(self, *args, **kwargs):
        super(TranscriptionForm, self).__init__(*args, **kwargs)
        # Set the 'text' field to be read-only
        self.fields['text'].disabled = True
        self.fields['title'].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance