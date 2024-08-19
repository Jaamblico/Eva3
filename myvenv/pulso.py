import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gpiozero import MCP3008
from time import sleep, time

# Initialize the MCP3008 device
ecg = MCP3008(0)

# Create a figure and three subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 12))
xs, ys = [], []

# Function to update the plot
def animate(i, xs, ys):
    # Read value from the MCP3008
    ecg_value = ecg.value
    
    # Add x and y values to lists
    current_time = time() - start_time
    xs.append(current_time)
    ys.append(ecg_value)
    print(ecg_value)
    
    # Limit lists to 1000 items
    xs = xs[-1000:]
    ys = ys[-1000:]
    
    # Clear subplots
    ax1.clear()
    ax2.clear()
    
    # Draw full data on the first subplot
    ax1.plot(xs, ys)
    ax1.set_title('ECG Signal (Full Duration)')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('ECG Value')
    
    # Draw last 30 seconds of data on the second subplot
    recent_xs = [x for x in xs if x >= current_time - 30]
    recent_ys = ys[-len(recent_xs):]
    ax2.plot(recent_xs, recent_ys)
    ax2.set_title('ECG Signal (Last 30 seconds)')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('ECG Value')
    
   
# Set up plot to call animate() function periodically
start_time = time()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=250)

# Display the plot
plt.tight_layout()
plt.show()
