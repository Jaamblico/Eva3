import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gpiozero import MCP3008
from time import sleep, time


# Initialize the MCP3008 device
ecg = MCP3008(0)

# Create a figure and three subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 15))
fig.patch.set_facecolor('darkseagreen')
xs, ys = [], []

ax1.set_facecolor('lightblue')
ax2.set_facecolor('lightgreen')

history = []
evenCount = 0
oddCount = 1

#PieChart
labels = ["Par","Impar"]
sizes = [evenCount,oddCount]
colors = ["blue", "green"]
pie_chart, texts,autotexts, = ax3.pie(sizes,labels=labels,colors=colors,autopct="%1.1f%%",startangle=90)


# Function to update the plot
def animate(i, xs, ys):
    global history, sizes,labels, colors, evenCount, oddCount

    # Read value from the MCP3008
    ecg_value = ecg.value

    history.append(int(ecg.value*100))
    #print(history)
    print(ecg.value)

##    if len(history)>6:
##        toss = sum(history[-6:])
##        print("La suma de los últimos 10 valores es: " + str(toss))
##        if toss % 2 == 0:
##            print("even")
##            evenCount += 1
##            history = []
##        else:
##            print("odd")
##            oddCount += 1
##            history = []

    #Update PieChart
    sizes = [evenCount/10,oddCount/10]
    ax3.clear()
    pie_chart, texts,autotexts, = ax3.pie(sizes,labels=labels,colors=colors,autopct="%1.1f%%",startangle=90)
    ax3.set_title("Porcentaje de números pares e impares")
##    for i, size in enumerate(sizes):
##        pie_chart[i].set_radius(size)
##        autotexts[i].set_text(f'{size:.1f}%')


    
    
    # Add x and y values to lists
    current_time = time() - start_time
    xs.append(current_time/2)
    ys.append(ecg_value)
    
    # Limit lists to 1000 items
    xs = xs[-1000:]
    ys = ys[-1000:]
    
    # Clear subplots
    ax1.clear()
    ax2.clear()
    
    # Draw full data on the first subplot
    ax1.plot(xs, ys,lw=2,color="green")
    ax1.set_title('Señal de la planta en el Tiempo')
    ax1.set_xlabel('Tiempo en segundos')
    ax1.set_ylabel('Valor de la Planta')
    
    # Draw last 30 seconds of data on the second subplot
    recent_xs = [x for x in xs if x >= current_time - 30]
    recent_ys = ys[-len(recent_xs):]
    ax2.plot(recent_xs, recent_ys,lw=2,color="blue")
    ax2.set_title('Últimos 30 segundos de la señal')
    ax2.set_xlabel('Tiempo en segundos')
    ax2.set_ylabel('Valor de la Planta')
    
   
# Set up plot to call animate() function periodically
start_time = time()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)

# Display the plot
plt.tight_layout()
plt.show()




