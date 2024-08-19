from gpiozero import MCP3008
from pythonosc import osc_message_builder
from pythonosc import udp_client
from time import sleep
import time
import argparse
import queue
import sys
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import os
import pyttsx3
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.response_synthesizers import ( ResponseMode, get_response_synthesizer)


q = queue.Queue()
grabando = False


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



# Initialize the MCP3008 device
ecg = MCP3008(0)

#client
sender = udp_client.SimpleUDPClient('127.0.0.1',4560)

def play_note(note):
    sender.send_message('/play_this', note)
    sleep(0.5)


tiempoPregunta = 10

while True:
    nota = ecg.value * 100
    play_note(nota)
    if ecg.value < 0.1 and grabando == False:
        start_time = time.time()
        while (time.time()-start_time) < tiempoPregunta:
            grabando = True
            print("grabando")
    if ecg.value > 0.1 and grabando == True:
        grabando = False

    print(ecg.value)
    print(grabando)


        
