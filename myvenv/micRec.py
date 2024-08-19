#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage using Dutch (nl) recognition model: `python test_microphone.py -m nl`
# For more help run: `python test_microphone.py -h`
import time
from time import sleep
import argparse
import queue
import sys
import json
import sounddevice as sd
from gpiozero import MCP3008
from vosk import Model, KaldiRecognizer

ecg = MCP3008(0)
grabando = False
tiempoPregunta = 10

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

def constArcano(data):
    rango = (1 - 0)
    nuevoRango = (22-1)
    arcano = (((data - 0)*nuevoRango) / rango)+1
    #print("el arcano es" + str(int(arcano)))
    return arcano
    

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

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        rec.SetWords(True)
        results = []
        history = []
        arcanos = []

        
        
        while True:
            print(ecg.value)
            history.append(ecg.value)
            sleep(0.125)
            if len(history) > 4:
                disparador = history[len(history)-1] + history[len(history)-2] + history[len(history)-3]+history[len(history)-4]+history[len(history)-5]+history[len(history)-6]+history[len(history)-7]+history[len(history)-8] 
                arcanos.append(constArcano(ecg.value))
                if disparador < 0.01 and grabando == False:
                    grabando = True
                    start_time = time.time()
                    while (time.time()-start_time) < tiempoPregunta:
                        history = []
                        data = q.get()
                        if rec.AcceptWaveform(data):
                            part_result = json.loads(rec.Result())
                            results.append(part_result)
                            print(rec.Result())
                        if dump_fn is not None:
                            dump_fn.write(data)
                        
                    #transcurrieron los 10''
                            
                    grabando = False
                    print("transcurrieron 10seg")
                    part_result = json.loads(rec.Result())
                    results.append(part_result)
                    text = ''
                    for r in results:
                        text += r['text'] + ' '
                    print(text)
                    results = []
                    arcanoFinal = arcanos[len(arcanos)-20]
                    print("el arcano final es" + str(arcanoFinal))
                    parser.exit(0)
                    with open('preguntas/pregunta.txt', 'w') as f:
                        f.truncate()
                        f.write(text)
                        #f.write("el arcano es " + str(int(arcanoFinal)))
                    

except KeyboardInterrupt:
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)
    text = ''
    for r in results:
        text += r['text'] + ' '
    print(text)
    #with open('preguntas/pregunta.txt', 'w') as f:
     #   f.write("")
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
