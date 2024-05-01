import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Create some data
x_data = np.linspace(0, 10, 100)
y_data = np.sin(x_data)

# Create a figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)

# Create a line plot
line, = ax.plot([], [], lw=2)

# Function to initialize the plot
def init():
    line.set_data([], [])
    return line,

# Function to update the plot for each frame
def update(frame):
    line.set_data(x_data[:frame], y_data[:frame])  # Show data up to current frame
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(x_data), init_func=init, blit=True, interval=50)

# If you want to save the animation to a file, you can uncomment the line below
# ani.save('animated_plot.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
