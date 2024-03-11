# Create your tasks here
from celery import shared_task
import whisper
from io import StringIO

@shared_task
def add(x, y):
    return x + y


@shared_task
def transcribe(file_path):
    model = whisper.load_model("base")
    file_path = file_path.replace('\\', '/')
    print(file_path)
    return 0