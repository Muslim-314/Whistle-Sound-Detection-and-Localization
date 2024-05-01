import numpy

def normalizedDb(sound_data, chunk_size):
    sound_data_fft = numpy.abs(numpy.fft.fft(sound_data)/2).astype(int)
    
    # calculate normalized db level
    for i in range(len(sound_data_fft)):
        if sound_data_fft[i] > 0:
            sound_data_fft[i] =  20 * (numpy.log10(sound_data_fft[i]) - numpy.log10(chunk_size * 32768))
        else:
            sound_data_fft[i] = -200
            
    return sound_data_fft
