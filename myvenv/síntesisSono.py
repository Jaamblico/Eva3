from gpiozero import MCP3008
from pythonosc import osc_message_builder
from pythonosc import udp_client
from time import sleep, time

# Initialize the MCP3008 device
ecg = MCP3008(0)

#client
sender = udp_client.SimpleUDPClient('127.0.0.1',4560)

def play_note(note):
    sender.send_message('/play_this', note)
    sleep(0.25)

def play_rythm(rit):
    sender.send_message('/play_that', rit)
    sleep(0.125)

while True:
    nota = ecg.value * 100
    ritmo = int(ecg.value * 10)
    play_note(nota)
    play_rythm(ritmo)
    print(nota)
    print(ritmo)
