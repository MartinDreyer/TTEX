from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .tasks import transcribe
import os
from django.urls import reverse
from django.contrib import messages



# Create your views here.


@login_required(redirect_field_name='')
def upload(request):
    return render(request, 'upload/upload.html', {})

def _prepare_file(request):
    try:
        audio_file, file_path = _save_audio_file(request)
        max_line_width = request.POST.get('format')
        return file_path, max_line_width
    except Exception as e:
        print(f"Error preparing file {e}")
        return None
    

def _save_audio_file(req):
    try:
        audio_file = req.FILES.get('audio_file', None)
        file_name = req.FILES.get('audio_file').name
        file_path = os.path.join(os.getcwd(), 'temp', 'audio', file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with default_storage.open(file_path, 'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        return audio_file, file_path
    except Exception as e:
        print(f"An error occurred while saving the audio file: {e}")
        return None, None

@login_required(redirect_field_name='')
def start_background_job(request):
    file_path, max_line_width = _prepare_file(request)
    try:
        transcribe.delay(
            file_path=file_path,
            username=str(request.user.get_username()),
            max_line_width=int(max_line_width)
        )
        return redirect('success')
    except Exception as e:
        print(f"An error occurred while saving the audio file: {e}")
        return redirect('retry')

 


@login_required(redirect_field_name='')
def success(request):
    return render(request, 'upload/success.html', {})

@login_required(redirect_field_name='')
def retry (request):
    return render(request, 'upload/retry.html', {})



