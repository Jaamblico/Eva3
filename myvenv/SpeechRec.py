import speech_recognition as sr

recognizer = sr.Recognizer()

audio_file = sr.AudioFile('EnIngles.wav')

with audio_file as source:
    audio_data = recognizer.record(source)

try:
    text = recognizer.recognize_sphinx(audio_data)
    print(f"Sphinx thinks you said: {text}")
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
