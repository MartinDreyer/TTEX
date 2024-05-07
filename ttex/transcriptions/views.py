from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from upload.models import Transcription
from .forms import TranscriptionForm
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


@login_required(redirect_field_name='')
def delete(request, id):
    transcription = Transcription.objects.get(id=id)
    transcription.delete()
    return render(request, 'transcriptions/transcription_deleted.html', {})

@login_required(redirect_field_name='')
def edit(request, id):
    transcription = get_object_or_404(Transcription, id=id)
    if request.method == "POST":
        form = TranscriptionForm(request.POST, instance=transcription)
        if form.is_valid():
            form.save()

            return redirect('detail', id=transcription.id)
    else:
        form = TranscriptionForm(instance=transcription)
        print(form.errors)  # Print form errors if any


    return render(request, 'transcriptions/edit.html', {'form': form})
    
@login_required(redirect_field_name='')
def download_transcription(request, id):
    transcription = Transcription.objects.get(id=id)
    response = HttpResponse(transcription.text, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{transcription.title}.srt"'
    return response
    