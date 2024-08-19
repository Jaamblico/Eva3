import os
import time
from time import sleep


fileHistory = []
n = 10

def detectFileChange():
    actual = os.path.getmtime("/home/martinmazzeo/Desktop/Projects/Eva3/myvenv/preguntas/pregunta.txt")
    fileHistory.append(actual)
    sleep(1)
    if fileHistory[len(fileHistory)-1] !=  fileHistory[len(fileHistory)-2]:
        modified = fileHistory[len(fileHistory)-1]
        print(modified)
    if len(fileHistory) > 10:
        del fileHistory[:n]

while True:
    detectFileChange()
