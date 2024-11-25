from gpiozero import MCP3008
from pythonosc import osc_message_builder
from pythonosc import udp_client
from time import sleep, time

# Initialize the MCP3008 device
ecg = MCP3008(0)

#client
sender = udp_client.SimpleUDPClient('127.0.0.1',4560)
pd_sender = udp_client.SimpleUDPClient('127.0.0.1',8000)

def play_note(note):
    sender.send_message('/play_this', note)
    sleep(0.25)

def playPDWave(w):
    pd_sender.send_message('/play_wave',float(w))
    sleep(0.05)
    

def findPrime(n):
    is_prime = 1
    if n > 1:
        is_prime = 1
        for i in range(2,int(n**0.5)+1):
            if(n%i) == 0:
                is_prime = 0
                break
        if is_prime:
            print(str(n)+" es Primo")
            
        else:
            print(str(n)+" no es Primo")
            
    else:
        print(str(n)+" no es Primo")

    return is_prime
                
##def tarotScale(n):
##
##    history = []
##    history.append(ecg.value)
##
##    if len(history) > 100:
##        
##    sleep(0.25)

def play_primo(n):
    sender.send_message('/play_primo', n)
    sleep(0.25)
 
def play_rythm(rit):
    sender.send_message('/play_that', rit)
    sleep(0.125)


#print(ecg.value)

while True:
    #nota = int(ecg.value * 100)
    #ritmo = int(ecg.value * 10)
    #print(primo)
    #play_primo(findPrime(int(ecg.value*10)))
    #print(findPrime(int(ecg.value*10)))
    playPDWave(ecg.value)
    print(ecg.value)
    #play_note(nota)
    #play_rythm(ritmo)
    #print("nota: " + str(nota))
    #print("ritmo: " + str(ritmo))
