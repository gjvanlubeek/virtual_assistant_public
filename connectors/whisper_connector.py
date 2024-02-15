import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class NoteTaker(object):
    def __init__(self, audiofile):
        self.audiofile = open(audiofile, "rb")

    def write_speech(self):
        result = client.audio.translations.create(
            model="whisper-1", 
            file=self.audiofile,
            response_format="text"
            )
        return result
    
if __name__ == '__main__':
    file = NoteTaker('output.wav')
    text = file.write_speech()
    print(text)
