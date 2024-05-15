import threading
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
CHUNK = 2**11 #2048 (16 Bit) sized buffer

#instantiate the microphones
p = pyaudio.PyAudio()
q = pyaudio.PyAudio()
r = pyaudio.PyAudio()

def lag_finder(y1, y2, sr):
    n = len(y1)
    corr = numpy.correlate(y2, y1, mode='same') / numpy.sqrt(numpy.correlate(y1, y1, mode='same')[int(n/2)] * numpy.correlate(y2, y2, mode='same')[int(n/2)])
    delay_arr = numpy.linspace(-0.5*n/sr, 0.5*n/sr, n)
    delay = delay_arr[numpy.argmax(corr)]
    return delay

streamp = p.open(format = pyaudio.paInt16,
                input_device_index = 2,
                channels = 1,
                rate = sampleRate,
                input = True,
                frames_per_buffer = CHUNK,
               )
streamq = q.open(format = pyaudio.paInt16,
                input_device_index = 3,
                channels = 1,
                rate = sampleRate,
                input = True,
                frames_per_buffer = CHUNK,
               )


# test the laptops MIC for testing remove SR when using code on 
streamr = r.open(format = pyaudio.paInt16,
                input_device_index = 4,
                channels = 1,
                rate = sampleRate,           #USED ONLY FOR PC IN-BUILT MIC USE sampleRate on Raspberry pi
                input = True,
                frames_per_buffer = CHUNK,
               )
sound_data_p = [0] *CHUNK
sound_data_q = [0] *CHUNK
sound_data_r = [0] *CHUNK
whistle_flag = False



# Init shutdown process on Ctrl+C 
print("Starting... use Ctrl+C to stop")
def handle_close(signum, frame):
    print("\nStopping")
    streamp.close()
    streamq.close()
    streamr.close()
    r.terminate()
    q.terminate()
    p.terminate()
    exit(1)
signal.signal(signal.SIGINT, handle_close)




# Thread for MIC-1 
def MIC1():
    global whistle_flag
    global sound_data_p
    global sound_data_q
    global sound_data_r
    i = 0
    while True:
        data_buffer_p = streamp.read(CHUNK, exception_on_overflow=False)
        sound_data_p = numpy.frombuffer(data_buffer_p, dtype=numpy.int16)
        y_fft_p = numpy.fft.fft(sound_data_p)
        y_fft_p = numpy.abs(y_fft_p).astype(int)
        if any(value > 8000000 for value in y_fft_p[1900:2000]):
            print("whistle MC1",i)
            i = i + 1
            whistle_flag = True
        
# Thread for MIC-2
def MIC2():
    global whistle_flag
    global sound_data_p
    global sound_data_q
    global sound_data_r
    i = 0
    while True:
        data_buffer_q = streamq.read(CHUNK, exception_on_overflow=False)
        sound_data_q = numpy.frombuffer(data_buffer_q, dtype=numpy.int16)
        y_fft_q = numpy.fft.fft(sound_data_q)
        y_fft_q = numpy.abs(y_fft_q).astype(int)
        if any(value > 8000000 for value in y_fft_q[1900:2000]):
            print("whistle MC2",i)
            i = i + 1
            whistle_flag = True    

# Thread for MIC-3
def MIC3():
    global whistle_flag
    global sound_data_p
    global sound_data_q
    global sound_data_r
    k = 0
    while True:
        data_buffer_r = streamr.read(CHUNK, exception_on_overflow=False)
        sound_data_r  = numpy.frombuffer(data_buffer_r, dtype=numpy.int16)
        y_fft_r = numpy.fft.fft(sound_data_r)
        y_fft_r = numpy.abs(y_fft_r).astype(int)
        if any(value > 8000000 for value in y_fft_r[1900:2000]):
            print("whistle MC3",k)
            k = k + 1
            whistle_flag = True
 
def mainProg():
    global whistle_flag
    global sound_data_p
    global sound_data_q
    global sound_data_r
    while True:
         if(whistle_flag == True):
             print("Sound data P:", sound_data_p)
             print("Sound data Q:", sound_data_q)
             print("Sound data R:", sound_data_r)
             t1 = lag_finder(sound_data_p,sound_data_q,sampleRate)
             t2 = lag_finder(sound_data_q,sound_data_r,sampleRate)
             t3 = lag_finder(sound_data_p,sound_data_r,sampleRate)
             print('Between p and q: t1 = ', t1)
             print('Between q and r: t2 = ', t2)
             print('Between p and r: t3 = ', t3)
         whistle_flag = False

 
thread1 = threading.Thread(target=MIC1)
thread2 = threading.Thread(target=MIC2)
thread3 = threading.Thread(target=MIC3)
thread4 = threading.Thread(target=mainProg)
# Start threading
thread1.start()
thread2.start()
thread3.start()
thread4.start()
#join threads
thread1.join()
thread2.join()
thread3.join()
thread4.join()
print("Main thread exiting...")

