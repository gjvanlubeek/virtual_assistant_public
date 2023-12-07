import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class NoteTaker :
    def __init__(self, audiofile):
        self.audiofile = open(audiofile, "rb")

    def write_speech(self):
        result = openai.Audio.translate("whisper-1", self.audiofile, response_format="text")
        return result
    
if __name__ == '__main__':
    file = NoteTaker('output.wav')
    text = file.write_speech()
    print(text)
