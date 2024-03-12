# Create your tasks here
from celery import shared_task
import whisper
from whisper.utils import WriteSRT
import os 
from pathlib import Path
from .models import Transcription
from django.contrib.auth.models import User
from django.core.mail import send_mail
from ttex import settings

@shared_task
def transcribe(file_path, username):
    """
    Transcribe an audio file to SRT format using Whisper and save the transcription.

    Args:
        file_path (str): The path to the audio file to transcribe.
        username (str): The username of the user who uploaded the audio file.

    Returns:
        None
    """
    # Load the Whisper model
    model = whisper.load_model("large", device="cpu")

    # Extract the file name from the file path and build the full path to the audio file
    file_name = file_path.split('\\')[-1]
    audio_path = os.path.join(os.getcwd(), 'temp', 'audio', file_name)

    # Prepare the output path for the SRT file
    srt_path = prepare_srt_path(audio_path)

    # Perform the transcription
    result = model.transcribe(f"file:{audio_path}", verbose=False)

    # Write the transcription result to an SRT file
    write_transcription_to_srt(srt_path, result)

    # Retrieve the user object
    user = User.objects.get(username=username)

    # Save the transcription to the database
    save_transcription(srt_path, user, audio_path)

def prepare_srt_path(audio_path):
    """
    Prepares the SRT file path based on the audio file path.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        Path: The path to the SRT file.
    """
    try:
        path = Path(audio_path)
        srt_path = path.parent.parent / 'srt' / (path.stem + '.srt')
        srt_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        return srt_path
    except Exception as e:
        print(f"An error occurred while preparing the SRT file path: {e}")

def write_transcription_to_srt(srt_path, result):
    """
    Writes the transcription result to an SRT file.

    Args:
        srt_path (Path): The path to the SRT file.
        result (dict): The transcription result from the Whisper model.

    Returns:
        None
    """
    try:
        srt_writer = WriteSRT(output_dir=srt_path.parent)
        with open(srt_path, "w") as f:
            srt_writer.write_result(result=result, file=f)
    except Exception as e:
        print(f"An error occurred while writing the transcription to the SRT file: {e}")

def notify_user(user_email, host):
        send_mail(
        subject = "TTEX",
        message="Din transskription er klar til download.",
        from_email=host,
        recipient_list=[user_email],
        fail_silently=False,
    )


def save_transcription(srt_path, user, audio_path):
    """
    Saves the transcription to the database and cleans up temporary files.

    Args:
        srt_path (Path): The path to the SRT file.
        user (User): The Django User object associated with the transcription.
        audio_path (str): The path to the audio file.

    Returns:
        None
    """
    try:
        with open(srt_path, "r") as f:
            srt_content = f.read()
            transcription = Transcription.objects.create(
                title=srt_path.stem,
                text=srt_content,
                user=user
            )

        # Send an email to the user to notify them that the transcription is ready
        try:
            notify_user(user.email, settings.EMAIL_HOST_USER)
        except Exception as e:
            print(f"An error occurred while sending the notification email: {e}")

        # Optionally save if you've modified the transcription instance further, otherwise this is not needed
        # transcription.save()

        # Clean up temporary files
        os.remove(audio_path)
        os.remove(srt_path)
    except Exception as e:
        print(f"An error occurred while saving the transcription: {e}")
        os.remove(audio_path)
        os.remove(srt_path)