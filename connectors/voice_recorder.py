import sounddevice as sd
from scipy.io.wavfile import write
 
class VoiceRecorder(object):
    def __init__(self, duration):
        self.fs = 11025 
        self.recordtime = duration
        self.channels = 1

    def record_voice(self):
        print("start recording") 
        myrecording = sd.rec(int(self.recordtime * self.fs), samplerate=self.fs, channels=self.channels)
        sd.wait()
        print("ended recording")
        write('output.wav', self.fs, myrecording)
