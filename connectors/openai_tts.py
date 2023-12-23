import os
from dotenv import load_dotenv

from pathlib import Path
from openai import OpenAI

from pydub import AudioSegment
from pydub.playback import play

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def generate_speech(text):
    speech_file_path = Path(__file__).parent / "../speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )

    response.stream_to_file(speech_file_path)

def play_mp3(file_path):
    sound = AudioSegment.from_file(file_path, format="mp3")
    play(sound)


if __name__ == '__main__':
    generate_speech("Hi Harmen, how are you doing?")
    play_mp3('speech.mp3')