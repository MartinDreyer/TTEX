from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from upload.models import Transcription
from .forms import TranscriptionForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator






# Create your views here.
@login_required(redirect_field_name='')
def index(request):
    q = request.GET.get('q', '')  # Retrieve 'q' from GET parameters
    if q:
        transcriptions = Transcription.objects.filter(
            user=request.user, title__icontains=q
        ).order_by("-created_at")
    else:
        transcriptions = Transcription.objects.filter(user=request.user).order_by("-created_at")
        
    # Pass a flag if there are no results
    no_results = not transcriptions.exists()
    
    p = Paginator(transcriptions, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    context = {
        'title': "Mine transkriberinger",
        'transcriptions': page_obj,
        'q': q,  # Pass the query to the template for use
        'no_results': no_results,  # Indicate if there are no results
    }
    return render(request, 'transcriptions/index.html', context)

def all(request):
    q = request.GET.get('q', '')  # Retrieve 'q' from GET parameters
    if q:
        transcriptions = Transcription.objects.all().filter(title__icontains=q).order_by("-created_at")
    else:
        transcriptions = Transcription.objects.all().order_by("-created_at")
        
    # Pass a flag if there are no results
    no_results = not transcriptions.exists()
    
    p = Paginator(transcriptions, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    context = {
        'title': "Alle transkriberinger",
        'transcriptions': page_obj,
        'q': q,  # Pass the query to the template for use
        'no_results': no_results,  # Indicate if there are no results
    }
    return render(request, 'transcriptions/index.html', context)

@login_required(redirect_field_name='')
def detail(request, id):
    transcription = get_object_or_404(Transcription, id=id)
    form = TranscriptionForm(instance=transcription)
    if request.method == "POST":
        form = TranscriptionForm(request.POST, instance=transcription)
        if form.is_valid():
            form.save()

        return redirect('detail', id=transcription.id)
    else:
            form = TranscriptionForm(instance=transcription)
            print(form.errors)  # Print form errors if any

    context = {
        'transcription': transcription,
        'form': form
        }

    return render(request, 'transcriptions/detail.html', context=context)

def not_found(request):
    return render(request, 'transcriptions/no_transcriptions_found.html', {})

@login_required(redirect_field_name='')
def delete(request, id):
    transcription = get_object_or_404(Transcription, id=id)
    transcription.delete()
    return render(request, 'transcriptions/transcription_deleted.html', {})

@login_required(redirect_field_name='')
def download_transcription(request, id):
    transcription = get_object_or_404(Transcription, id=id)
    response = HttpResponse(transcription.text, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{transcription.title}.srt"'    
    