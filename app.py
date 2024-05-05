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

#instantiate the microphones
p = pyaudio.PyAudio()
q = pyaudio.PyAudio()
r = pyaudio.PyAudio()


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

stream = q.open(format = pyaudio.paInt16,
                channels = 1,
                rate = sampleRate,
                input = True,
                frames_per_buffer = CHUNK,
               )
stream = r.open(format = pyaudio.paInt16,
                channels = 1,
                rate = sampleRate,
                input = True,
                frames_per_buffer = CHUNK,
               )

# plotter = FFT_Normalized_DB_Plotter(CHUNK, sampleRate) 
plotter_p= FFT_Plotter(CHUNK, sampleRate)
plotter_q= FFT_Plotter(CHUNK, sampleRate)
plotter_r= FFT_Plotter(CHUNK, sampleRate)
# Init shutdown process on Ctrl+C 
print("Starting... use Ctrl+C to stop")
def handle_close(signum, frame):
    print("\nStopping")
    plotter_p.close()
    plotter_q.close()
    plotter_r.close()
    stream.close()
    p.terminate()
    exit(1)
signal.signal(signal.SIGINT, handle_close)
i = 0
j = 0
k = 0 
# Listen to Sound Input
while True:
    #computation for first microphone(p)
    data_buffer_p = stream.read(CHUNK, exception_on_overflow=False)
    sound_data_p = numpy.frombuffer(data_buffer_p, dtype=numpy.int16)
    y_fft_p = numpy.fft.fft(sound_data_p)
    y_fft_p = numpy.abs(y_fft_p).astype(int)
    plotter_p.plot(y_fft_p)
    if any(value > 400000 for value in y_fft_p[1850:2000]):
        print("whistle MC1",i)
        i = i + 1


    #computation for first microphone(q)
    data_buffer_q = stream.read(CHUNK, exception_on_overflow=False)
    sound_data_q = numpy.frombuffer(data_buffer_q, dtype=numpy.int16)
    y_fft_q = numpy.fft.fft(sound_data_p)
    y_fft_q = numpy.abs(y_fft_q).astype(int)
    plotter_q.plot(y_fft_q)
    if any(value > 400000 for value in y_fft_q[1850:2000]):
        print("whistle MC2",j)
        j = j + 1

    #computation for first microphone(p)
    data_buffer_r = stream.read(CHUNK, exception_on_overflow=False)
    sound_data_r  = numpy.frombuffer(data_buffer_r, dtype=numpy.int16)
    y_fft_r = numpy.fft.fft(sound_data_r)
    y_fft_r = numpy.abs(y_fft_r).astype(int)
    plotter_r.plot(y_fft_r)
    if any(value > 400000 for value in y_fft_r[1850:2000]):
        print("whistle MC3",k)
        k = k + 1

        #finding the freq for which the magnitude is greater than threshold
        # indexes_above_threshold = numpy.where(y_fft > 30000)[0]
        # if len(indexes_above_threshold) > 0:
        #     print("Whistle detected at indexes:", indexes_above_threshold)
        



 



