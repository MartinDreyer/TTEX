# Create your tasks here
from celery import shared_task
import whisper
from whisper.utils import WriteSRT
import os
from pathlib import Path
from .models import Transcription
from django.contrib.auth.models import User
from ttex import settings
import requests
import uuid
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from ttex.utils import get_secret
from requests.models import PreparedRequest  # For URL validation
import logging
from dotenv import load_dotenv
logger = logging.getLogger(__name__)

load_dotenv()


MODEL_SIZE = os.environ.get("MODEL_SIZE", "small")
DEVICE = os.environ.get("DEVICE", "cpu")
DOWNLOAD_ROOT = os.environ.get("DOWNLOAD_FOLDER", "ttex/models")

@shared_task
def transcribe(file_path, username, max_line_width=42):
    """
    Transcribe an audio file to SRT format using Whisper and save the transcription.

    Args:
        file_path (str): The path to the audio file to transcribe.
        username (str): The username of the user who uploaded the audio file.
        (optional) max_line_width (int): The maximum length of each line in the srt. 

    Returns:
        None
    """
    # Get variables
    user, model, file_name, audio_path, srt_path = get_variables(username=username, file_path=file_path)

    # Create a pending transcription
    transcription = create_pending(file_path=file_path, user=user)
    id = transcription.id

    # Create the actual transcription
    result = create_transcription(model=model, audio_path=audio_path)

    # Create SRT and save it to transcription.
    if result and srt_path:
        try:
            write_transcription_to_srt(srt_path, result, max_line_width=max_line_width)
            save_transcription(srt_path, user, audio_path, id)
        except Exception as e:
            print(f"Error saving transcription {e}")
            return

    
def create_transcription(model, audio_path):
    try:
        result = model.transcribe(
            f"file:{audio_path}", verbose=False, word_timestamps=True)
        return result
    except Exception as e:
        print(f"An error occurred while transcribing the audio file: {e}")
        return

def get_variables(username, file_path):
    user = User.objects.get(username=username)
    model = whisper.load_model(MODEL_SIZE, device=DEVICE, download_root=DOWNLOAD_ROOT)
    file_name = file_path.split('\\')[-1]
    audio_path = os.path.join(os.getcwd(), 'temp', 'audio', file_name)
    srt_path = prepare_srt_path(audio_path)

    return user, model, file_name, audio_path, srt_path

def create_pending(file_path, user):
    try:
        transcription = Transcription.objects.create(
        title=Path(file_path).stem,
        user=user,
        status="PENDING",
        text="Transskribering undervejs ..."
    )
        transcription.save()
        return transcription
    except Exception as e:
        print(f"Error creating pending transcription {e}")
        return 


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
        # Ensure the directory exists
        srt_path.parent.mkdir(parents=True, exist_ok=True)
        return srt_path
    except Exception as e:
        print(f"An error occurred while preparing the SRT file path: {e}")


def write_transcription_to_srt(srt_path, result, max_line_width):
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
            srt_writer.write_result(
                result=result, file=f, max_line_count=1, max_line_width=max_line_width)
    except Exception as e:
        print(
            f"An error occurred while writing the transcription to the SRT file: {e}")


def notify_user(user_email, transcription_title):
    url = get_secret("NOTIFICATION_URL")
    try:
        req = PreparedRequest()
        req.prepare_url(url, None)
        if not req.url:
            raise ValueError("Invalid URL")
    except Exception as e:
        print(f"Invalid URL: {e}")
        return
    tenant_id = get_secret("MICROSOFT_AUTH_TENANT_ID")
    client_id = get_secret("MICROSOFT_AUTH_CLIENT_ID")
    client_secret = get_secret("MICROSOFT_AUTH_CLIENT_SECRET")
    # fmt: off
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    # fmt: on

    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url,
                              client_id=client_id,
                              client_secret=client_secret,
                              scope=[
                                  "https://service.flow.microsoft.com//.default"],
                              )

    access_token = token["access_token"]

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    data = {
        "email": user_email,
        "message": f"Din transskribering af {transcription_title} er klar! <br><br> <i>Denne mail kan ikke besvares</i>"
    }
    try:
        res = requests.post(url, json=data, headers=headers)
        if res.status_code != 202:
            print(
                f"An error occurred while sending the notification: {res.text}")
        else:
            print("Notification sent successfully")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the notification: {e}")


def save_transcription(srt_path, user, audio_path, id):
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

            transcription = Transcription.objects.get(id=id)
            transcription.text = srt_content
            transcription.status = "COMPLETE"
            transcription.save()

        # Send an email to the user to notify them that the transcription is ready
        try:
            notify_user(user.email, transcription.title)
        except Exception as e:
            print(
                f"An error occurred while sending the notification email: {e}")

        # Optionally save if you've modified the transcription instance further, otherwise this is not needed
        # transcription.save()

        # Clean up temporary files
        os.remove(audio_path)
        os.remove(srt_path)
    except Exception as e:
        print(f"An error occurred while saving the transcription: {e}")
        os.remove(audio_path)
        os.remove(srt_path)
