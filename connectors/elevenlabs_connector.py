import os
from dotenv import load_dotenv
from elevenlabs import generate, play
from elevenlabs import set_api_key
 
load_dotenv()
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

class DigitalVoice:
    def __init__(self, text):
        self.text = text
        self.voice = "Dorothy"
        self.model = "eleven_multilingual_v2"
        self.speech = None

    def generate_speech(self):
        self.speech = generate(
            text=self.text,
            voice=self.voice,
            model=self.model
        )

    def play_speech(self):
        print(self.text)
        play(self.speech)