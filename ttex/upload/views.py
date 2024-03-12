from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .tasks import transcribe
import os

# Create your views here.

@login_required(redirect_field_name='')
def upload(request):
    return render(request, 'upload/upload.html', {})


def _save_audio_file(req):
    audio_file = req.FILES.get('audio_file', None)
    file_name = req.FILES.get('audio_file').name
    file_path = os.path.join(os.getcwd(), 'temp', 'audio', file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True) 
    with default_storage.open(file_path, 'wb') as destination:
        for chunk in audio_file.chunks():
            destination.write(chunk)
    return audio_file, file_path


@login_required(redirect_field_name='')
def start_background_job(request):
    audio_file, file_path = _save_audio_file(request)
    if not audio_file:
        return HttpResponse(content="No file found!", status=400)
    else:
        transcribe.delay(file_path, username=(str(request.user.get_username())))
        return redirect('succes')
    
@login_required(redirect_field_name='')
def succes(request):
    return render(request, 'upload/succes.html', {})
