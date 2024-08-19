import time
from time import sleep
from gpiozero import MCP3008

ecg = MCP3008(0)


def plantData(data):
    rango = (1 - 0)
    nuevoRango = (22-1)
    arcano = (((data - 0)*nuevoRango) / rango)+1
    print(int(arcano))
    with open('preguntas/pregunta.txt', 'w') as f:
                            f.write(arcano)

        
while True:
    print(ecg.value)
    plantData(ecg.value)
    sleep(0.25)
