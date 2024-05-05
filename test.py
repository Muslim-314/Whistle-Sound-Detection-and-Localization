import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16 bits per sample)
CHANNELS = 1  # Single channel for microphone input
RATE = 44100  # Sampling rate in Hz

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Create figure for plotting
fig, ax = plt.subplots()
x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))

# Customize plot
ax.set_ylim(0, 255)
ax.set_xlim(0, CHUNK)

# Function to update the plot
def update_plot(frame):
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    y = np.fft.fft(data)
    line.set_ydata(np.abs(y[0:CHUNK]) * 2 / (256 * CHUNK))
    return line,

# Start the animation
ani = FuncAnimation(fig, update_plot, blit=True)
plt.show()

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()

