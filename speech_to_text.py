import speech_recognition as sr
from os import path

#filename = ""
#audio_file = path.join(path.dirname(path.realpath(__file__)), filename)
#audio = sr.AudioData.from_file(audio_file)

r = sr.Recognizer()

with sr.Microphone() as source:
    audio = r.listen(source)

text = r.recognize_amazon(audio)


a = 4