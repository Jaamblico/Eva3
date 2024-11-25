import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gpiozero import MCP3008
from time import sleep, time


# Initialize the MCP3008 device
ecg = MCP3008(0)

# Create a figure and three subplots
fig, (ax1) = plt.subplots(1, 1, figsize=(9, 6))
fig.patch.set_facecolor('darkseagreen')
xs, ys = [], []

ax1.set_facecolor('lightblue')




def animate(i, xs, ys):
    global sizes,labels, colors

   
    ecg_value = ecg.value

    
    
    # Add x and y values to lists
    current_time = time() - start_time
    xs.append(current_time/2)
    ys.append(ecg_value)
    
    # Limit lists to 1000 items
    xs = xs[-100:]
    ys = ys[-100:]
    
    # Clear subplots
    ax1.clear()

    
    # Draw full data on the first subplot
    ax1.plot(xs, ys,lw=2,color="green")
    ax1.set_title('Señal de la planta en el Tiempo')
    ax1.set_xlabel('Tiempo en segundos')
    ax1.set_ylabel('Valor de la Planta')
    
    
    
   
# Set up plot to call animate() function periodically
start_time = time()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=50)

# Display the plot
plt.tight_layout()

plt.show()




