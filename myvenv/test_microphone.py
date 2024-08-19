# MicRec
import time
from time import sleep
import argparse
import queue
import sys
import json
import sounddevice as sd
from gpiozero import MCP3008
from gpiozero import LED
from vosk import Model, KaldiRecognizer

ecg = MCP3008(0)
grabando = False
tiempoPregunta = 10
mainHistory = []
lifeCicles = ["NEUTRO"]
umbral = 7
recLed = LED(4)

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def chooseHexagram(data):
    rango = (1 - 0)
    nuevoRango = (64-1)
    hexagrama = int((((data - 0)*nuevoRango) / rango)+1)
    #print("el hexagrama es el: " + str(int(hexagrama)))
    return hexagrama

def moodDetector(value):
    global mainHistory, lifeCicles
    mainHistory.append(value*10)
    if len(mainHistory) > 30:
        diferencia = max(mainHistory) - min(mainHistory)
        print("La diferencia es: " + str(diferencia))
        mainHistory = []
        if diferencia > umbral:
            print("CAOS-ESTRËS-FRIO")
            lifeCicles.append("CAOS")
        else:
            print("CALMA-RELAX-CALOR")
            lifeCicles.append("ORDEN")

    return lifeCicles

def start_recording():
    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        sleep(1)
        start_time = time.time()
        history = []
        while (time.time()-start_time) < tiempoPregunta:
            recLed.on()
            
            data = q.get()
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                results.append(part_result)
                print(rec.Result())
        recLed.off()
        text = ''
        for r in results:
            text += r['text'] + ' '
        print(text)
        with open('preguntas/pregunta.txt', 'w') as f:
            f.truncate()
            f.write(text)
            f.write("El hexagrama es el: " + str(hexagramas[len(hexagramas)-16]) + " ")
            if actualMood == "CAOS":
                f.write("disminuye la temperatura del modelo en 0.1")
            else:
                f.write("aumenta la temperatura del modelo en 0.1")
        results.clear()

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model('model')
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

        rec = KaldiRecognizer(model, args.samplerate)
        rec.SetWords(True)
        results = []
        history = []
        hexagramas = []
        disparador = 0
        
        while True:
            hexa = chooseHexagram(ecg.value)
            hexagramas.append(hexa)
            moodHistory = moodDetector(ecg.value)
            actualMood = moodHistory[len(moodHistory)-1]
            print(ecg.value)
            #print(moodHistory)
            #print(actualMood)
            history.append(ecg.value)
            if len(history) > 30:
                disparador = sum(history[-30:])
                #print(disparador)
                if disparador > 27 and grabando == False:
                    grabando = True
                    disparador = 0
                    history = []
                    start_recording()
                    grabando = False
                    sleep(1)
                else:
                    print(rec.PartialResult())
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
