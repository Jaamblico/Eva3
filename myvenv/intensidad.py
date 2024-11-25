from gpiozero import MCP3008
from gpiozero import PWMLED
from time import sleep

ecg = MCP3008(0)
led = PWMLED(4)

led.off()
sleep(3)

while True:
    led.value = ecg.value
    #sleep(0.125)
    print(ecg.value)
