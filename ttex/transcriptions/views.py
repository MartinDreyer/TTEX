from django.shortcuts import render
from upload.models import Transcription
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(redirect_field_name='')
def index(request):
    transcriptions = Transcription.objects.all()
    context = {
        'transcriptions': transcriptions
    }
    return render(request, 'transcriptions/index.html', context)

@login_required(redirect_field_name='')
def detail(request, id):
    transcription = Transcription.objects.get(id=id)
    context = {
        'transcription': transcription
    }
    return render(request, 'transcriptions/detail.html', context)