from gpiozero import MCP3008
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from collections import deque
import numpy as np
from time import sleep

# Initialize ADC and data collection
ecg = MCP3008(0)
readings_buffer = deque(maxlen=10)
odd_count = 0
even_count = 0

# Setup plot and circle
fig, ax = plt.subplots()
circle = Circle((0.5, 0.5), 0.1, facecolor='blue', edgecolor='black')
ax.add_patch(circle)
ax.set_aspect('equal')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.ion()  # Turn on interactive mode for animation

while True:
    # Read ECG value
    ecg_value = ecg.value
    
    # Store the value in buffer
    readings_buffer.append(ecg_value)
    
    # Count odd and even readings in the buffer
    odd_count = sum(1 for x in readings_buffer if x % 2 != 0)
    even_count = len(readings_buffer) - odd_count
    
    # Determine majority
    if odd_count > even_count:
        circle.set_facecolor('blue')
    else:
        circle.set_facecolor('red')
    
    # Update plot
    plt.draw()
    plt.pause(0.001)
    
    sleep(0.125)  # Adjust sleep time as needed
