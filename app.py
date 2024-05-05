import sys
import signal
import numpy
import pyaudio
import matplotlib.pyplot as plt
sys.path.append("src")
from plotter import FFT_Plotter, FFT_Normalized_DB_Plotter
from normalized_db import normalizedDb

sys.path.remove("src")
sampleRate = 44100
p = pyaudio.PyAudio()

# the size of buffer
# if you have a samplerate of 48000 per second and your buffer size is 2048
# then the FFT applies every 2048/48000(s) = ~0,043 seconds
CHUNK = 2**11 # =2048
 


stream = p.open(format = pyaudio.paInt16,
                channels = 1,
                rate = sampleRate,
                input = True,
                frames_per_buffer = CHUNK,
               )

# plotter = FFT_Normalized_DB_Plotter(CHUNK, sampleRate) 
plotter= FFT_Plotter(CHUNK, sampleRate)

# Init shutdown process on Ctrl+C 
print("Starting... use Ctrl+C to stop")
def handle_close(signum, frame):
    print("\nStopping")
    plotter.close()
    stream.close()
    p.terminate()
    exit(1)
signal.signal(signal.SIGINT, handle_close)
i = 0

# Listen to Sound Input
while True:
    data_buffer = stream.read(CHUNK, exception_on_overflow=False)
    sound_data = numpy.frombuffer(data_buffer, dtype=numpy.int16)
    #### PLOT AMPLITUDE ####
    y_fft = numpy.fft.fft(sound_data)
    y_fft = numpy.abs(y_fft).astype(int)
    plotter.plot(y_fft)
    if any(value > 400000 for value in y_fft[1850:2000]):
        print("whistle ",i)
        i = i + 1
        
        #finding the freq for which the magnitude is greater than threshold
        # indexes_above_threshold = numpy.where(y_fft > 30000)[0]
        # if len(indexes_above_threshold) > 0:
        #     print("Whistle detected at indexes:", indexes_above_threshold)
        



 



