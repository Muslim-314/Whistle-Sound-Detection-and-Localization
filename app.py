import sys
import signal
import numpy 
import pyaudio
import scipy
import matplotlib.pyplot as plt
sys.path.append("src")
from plotter import FFT_Plotter, FFT_Normalized_DB_Plotter
from normalized_db import normalizedDb
sys.path.remove("src")
sampleRate = 44100

def lag_finder(y1, y2, sr):
    n = len(y1)

    corr = numpy.correlate(y2, y1, mode='same') / numpy.sqrt(numpy.correlate(y1, y1, mode='same')[int(n/2)] * numpy.correlate(y2, y2, mode='same')[int(n/2)])

    delay_arr = numpy.linspace(-0.5*n/sr, 0.5*n/sr, n)
    delay = delay_arr[numpy.argmax(corr)]
    return delay




#instantiate the microphones
p = pyaudio.PyAudio()
q = pyaudio.PyAudio()
r = pyaudio.PyAudio()


# the size of buffer
# if you have a samplerate of 48000 per second and your buffer size is 2048
# then the FFT applies every 2048/48000(s) = ~0,043 seconds
CHUNK = 2**11 # =2048
 
streamp = p.open(format = pyaudio.paInt16,
                input_device_index = 1,
                channels = 1,
                rate = sampleRate,
                input = True,
                frames_per_buffer = CHUNK,
               )

streamq = q.open(format = pyaudio.paInt16,
                input_device_index = 2,
                channels = 1,
                rate = sampleRate,
                input = True,
                frames_per_buffer = CHUNK,
               )
streamr = r.open(format = pyaudio.paInt16,
                input_device_index = 3,
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
    streamp.close()
    p.terminate()
    streamq.close()
    q.terminate()
    streamr.close()
    r.terminate()
    exit(1)
signal.signal(signal.SIGINT, handle_close)
i = 0
j = 0
k = 0 
# Listen to Sound Input
whistle_FlagP = False
whistle_FlagQ = False
whistle_FlagR = False
while True:
    #computation for first microphone(p)3
    data_buffer_p = streamp.read(CHUNK, exception_on_overflow=False)
    sound_data_p = numpy.frombuffer(data_buffer_p, dtype=numpy.int16)
    y_fft_p = numpy.fft.fft(sound_data_p)
    #y_fft_p = numpy.abs(y_fft_p).astype(int)
    #plotter_p.plot(y_fft_p)
    if any(value > 8000000 for value in y_fft_p[1900:2000]):
        whistle_FlagP = True
        print("whistle MC1",i)
        i = i + 1
    else:
        whistle_FlagP = False

    #computation for first microphone(q)
    data_buffer_q = streamq.read(CHUNK, exception_on_overflow=False)
    sound_data_q = numpy.frombuffer(data_buffer_q, dtype=numpy.int16)
    y_fft_q = numpy.fft.fft(sound_data_q)
    #y_fft_q = numpy.abs(y_fft_q).astype(int)
    #plotter_q.plot(y_fft_q)
    if any(value > 8000000 for value in y_fft_q[1900:2000]):
        whistle_FlagQ = True
        print("whistle MC2",j)
        j = j + 1
    else:
        whistle_FlagQ = False
    #computation for first microphone(p)
    data_buffer_r = streamr.read(CHUNK, exception_on_overflow=False)
    sound_data_r  = numpy.frombuffer(data_buffer_r, dtype=numpy.int16)
    y_fft_r = numpy.fft.fft(sound_data_r)
    #y_fft_r = numpy.abs(y_fft_r).astype(int)
    #plotter_r.plot(y_fft_r)
    if any(value > 8000000 for value in y_fft_r[1900:2000]):
        whistle_FlagR = True
        print("whistle MC3",k)
        k = k + 1
    else:
        whistle_FlagR = False
        
    if (whistle_FlagP == True and whistle_FlagQ == True and whistle_FlagR == True):    
        time_delayPR = lag_finder(sound_data_p,sound_data_q,CHUNK)
        time_delayQR = lag_finder(sound_data_q, sound_data_r, CHUNK)
        if (time_delayPR > time_delayQR):
            print("Sound from right side")
        else:
            print("Soudn from the left side")
            
        #finding the freq for which the magnitude is greater than threshold
        # indexes_above_threshold = numpy.where(y_fft > 30000)[0]
        # if len(indexes_above_threshold) > 0:
        #     print("Whistle detected at indexes:", indexes_above_threshold)
        



 



