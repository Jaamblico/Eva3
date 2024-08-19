import wave
import json
from vosk import Model, KaldiRecognizer




wf = wave.open('EspañolOraculoTest.wav', "rb")
model = Model('model')
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

results = []
# recognize speech using vosk model
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)

part_result = json.loads(rec.FinalResult())
results.append(part_result)

# forming a final string from the words
text = ''
for r in results:
    text += r['text'] + ' '

print(f"Vosk thinks you said:\n {text}")

with open('respuestas/respuesta.txt', 'w') as f:
    f.write(text)
