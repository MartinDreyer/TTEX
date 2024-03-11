from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .tasks import add, transcribe
from django.core.files.storage import default_storage
import os

# Create your views here.
@login_required
def upload(request):
    return render(request, 'upload/upload.html', {})


def start_background_job(request):
    audio_file = request.FILES.get('audio_file', None)
    file_name = request.FILES.get('audio_file').name
    if not audio_file:
        return HttpResponse(content="No file found!", status=400)
    else:
        file_path = os.path.join(os.getcwd(), 'temp', file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Replace with your desired file path
        with default_storage.open(file_path, 'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        transcribe.delay(file_path)
        add.delay(4, 4)
        return HttpResponse(content="Job started successfully!", status=200)