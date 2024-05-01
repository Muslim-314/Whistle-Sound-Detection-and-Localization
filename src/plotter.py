import matplotlib # <= mac fix
matplotlib.use("TkAgg") # <= mac fix
import matplotlib.pyplot as plt
import numpy

class FFT_Plotter:
    def __init__(self, CHUNK, sampleRate):
        fig, ax = plt.subplots()

        # get X-Axis Freuqncies in Hz
        # fftfreq returns list of coefficients (c),
        # Hz-freq[i] = abs(c[i] * sampleRate)
        coefficients = numpy.fft.fftfreq(CHUNK)
        x_freq = [ numpy.abs(c * sampleRate) for c in coefficients ]

        # for y axis the initial will be CHUNK size array with random values
        highest_random_numer = numpy.iinfo(numpy.int16).max*10
        y_random = numpy.random.randint(low=0, high=highest_random_numer, size=CHUNK)

        # plot an get line object
        line, = ax.plot(x_freq, y_random)

        # style plot
        ax.set_xlim(0, sampleRate/4)
        plt.xlabel("Freq [Hz]")
        plt.ylabel("Amplitude / FFT Magnitude")
        plt.show(block=False)

        # assign class variables
        self.fig = fig
        self.line = line

    # y values for the graph to plot, must have length of CHUNK
    # y should be result of FFT
    def plot(self, y):
        self.line.set_ydata(y)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def close(self):
        plt.close(self.fig)


class FFT_Normalized_DB_Plotter:
    def __init__(self, CHUNK, sampleRate):
        fig, ax = plt.subplots()

        # get X-Axis Freuqncies in Hz
        coefficients = numpy.fft.fftfreq(CHUNK)
        x_freq = [ numpy.abs(c * sampleRate) for c in coefficients ]

        # start from -240 to 0 DB, random values
        y_random = numpy.random.randint(low=240*-1, high=0, size=CHUNK)

        line, = ax.plot(x_freq, y_random)

        # style plot
        ax.set_xlim(0, sampleRate/4)
        plt.xlabel("Freq [Hz]")
        plt.ylabel("Normalied Sound Pressure Level [dB]")
        plt.show(block=False)

        self.fig = fig
        self.line = line

    # y should be result of normaliedDb(FFT)
    def plot(self, y):
        self.line.set_ydata(y)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def close(self):
        plt.close(self.fig)
