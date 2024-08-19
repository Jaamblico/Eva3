from gpiozero import MCP3008

ecg = MCP3008(0)
ciclos = []

def tirada(ciclo):

    hexagrama = []
    
    for i in range(6):
        i = 0
        hexagrama.append(i)
        
    # Primer Trigrama

    if ciclo[0] %2 == 0:
        hexagrama[0] = "0"
        print("-----   -----")
    else:
        hexagrama[0] = "1"
        print("-------------")

    if ciclo[1] %2 == 0:
        hexagrama[1] = "0"
        print("-----   -----")
    else:
        hexagrama[1] = "1"
        print("-------------")
##
    if ciclo[2] %2 == 0:
        hexagrama[2] = "0"
        print("-----   -----")
    else:
        hexagrama[2] = "1"
        print("-------------")

    # Segundo Trigrama

    if ciclo[3] %2 == 0:
        hexagrama[3] = "0"
        print("-----   -----")
    else:
        hexagrama[3] = "1"
        print("-------------")

    if ciclo[4] %2 == 0:
        hexagrama[4] = "0"
        print("-----   -----")
    else:
        hexagrama[4] = "1"
        print("-------------")

    if ciclo[5] %2 == 0:
        hexagrama[5] = "0"
        print("-----   -----")
    else:
        hexagrama[5] = "1"
        print("-------------")

    print(hexagrama)
    return hexagrama

for x in range(6):
    ciclos.append(int(ecg.value*100))

print(ciclos)
tirada(ciclos)


