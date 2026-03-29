import speech_recognition as sr
from os import path
import whisper

#filename = ""
#audio_file = path.join(path.dirname(path.realpath(__file__)), filename)
#audio = sr.AudioData.from_file(audio_file)

r = sr.Recognizer()
model = whisper.load_model("turbo")

def main(audio, timestamps):
    text = ""
    for i in range(len(timestamps) - 1):
        audio_chunk = audio[timestamps[i][0]:timestamps[i+1][0]]
        #text1 = r.recognize_whisper(audio_chunk)
        text1 = model.transcribe(audio_chunk, language="english")["text"]
        text1 = timestamps[i][1] + ": " + text1
        text += text1 + "\n"
    return text





a = 4