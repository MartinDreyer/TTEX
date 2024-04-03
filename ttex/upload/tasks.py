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

@shared_task
def transcribe(file_path, username, max_line_width=42):
    """
    Transcribe an audio file to SRT format using Whisper and save the transcription.

    Args:
        file_path (str): The path to the audio file to transcribe.
        username (str): The username of the user who uploaded the audio file.

    Returns:
        None
    """


    # Create pending transcription instance
    user = User.objects.get(username=username)
    id = uuid.uuid4()

    # Create a pending transcription instance
    transcription = Transcription.objects.create(
        id=id,
        title=Path(file_path).stem,
        user=user,
        status="PENDING",
        text="Transskribering undervejs ..."
    )
    transcription.save()

    # Load the Whisper model
    model = whisper.load_model("base", device="cpu")

    # Extract the file name from the file path and build the full path to the audio file
    file_name = file_path.split('\\')[-1]
    audio_path = os.path.join(os.getcwd(), 'temp', 'audio', file_name)

    # Prepare the output path for the SRT file
    srt_path = prepare_srt_path(audio_path)

    # Perform the transcription
    result = model.transcribe(f"file:{audio_path}", verbose=False, word_timestamps=True)

    # Write the transcription result to an SRT file
    write_transcription_to_srt(srt_path, result, max_line_width=max_line_width)


    # Save the transcription to the database
    save_transcription(srt_path, user, audio_path, id)

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
            srt_writer.write_result(result=result, file=f, max_line_count=1, max_line_width=max_line_width)
    except Exception as e:
            print(f"An error occurred while writing the transcription to the SRT file: {e}")

def notify_user(user_email):
    url = os.environ.get("NOTIFICATION_URL")
    headers = {
        
    }
    data = {
        "email": user_email,
    }
    try:
        res = requests.post(url, json=data)
        if res.status_code != 200:
            print(f"An error occurred while sending the notification: {res.text}")
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

    def add_hyphens(srt_content):
        lines = srt_content.split('\n')  # Split the content into lines
        modified_lines = []

        for i, line in enumerate(lines):
            # Check if the line starts with an alphabetic character
            if line and line[0].isalpha():
                # Add '- ' to the end of the line if it doesn't end with a period
                if not line.endswith('.'):
                    line += ' -'

                modified_lines.append(line)
            else:
                modified_lines.append(line)

        for i in range(1, len(modified_lines)):
            # Add '- ' to the start of the line if it starts with a lowercase letter
            # Ensure the line starts with an alphabetic character
            if modified_lines[i] and modified_lines[i][0].isalpha() and modified_lines[i][0].islower():
                modified_lines[i] = '- ' + modified_lines[i]
            else:
                modified_lines[i] = modified_lines[i]

        # Join the lines back into a single string
        modified_content = '\n'.join(modified_lines)
        return modified_content

    try:
        with open(srt_path, "r") as f:
            srt_content = f.read()
            srt_content = add_hyphens(srt_content)

            transcription = Transcription.objects.get(id=id)
            transcription.text = srt_content
            transcription.text = srt_content
            transcription.status = "COMPLETE"
            transcription.save()

        # Send an email to the user to notify them that the transcription is ready
        try:
            notify_user(user.email)
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