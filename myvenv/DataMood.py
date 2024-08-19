from gpiozero import MCP3008
from time import sleep

ecg = MCP3008(0)
mainHistory = []
lifeCicles = []
umbral = 7


def moodDetector(value):
    global mainHistory, lifeCicles
    mainHistory.append(value*10)
    print(value)
    if len(mainHistory) > 30:
        diferencia = max(mainHistory) - min(mainHistory)
        print("La umbral es: 7")
        print("La diferencia es: " + str(diferencia))
        mainHistory = []
        if diferencia > umbral:
            print("CAOS-ESTRËS-FRIO")
            lifeCicles.append("CAOS")
        else:
            print("CALMA-RELAX-CALOR")
            lifeCicles.append("ORDEN")

    return lifeCicles


while True:
    print(moodDetector(ecg.value))
    sleep(0.25)
