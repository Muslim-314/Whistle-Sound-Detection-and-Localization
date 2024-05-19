# Whistle Detection and Localization System

## Introduction

This project aims to develop a whistle detection and localization system using multiple microphones and signal processing techniques. The system utilizes three microphones to capture audio signals, processes these signals to detect whistles, and determines the direction of the detected whistle sound. The project leverages Python for audio processing and threading for concurrent execution.

## System Setup and Libraries

The system uses several libraries:
- `pyaudio` for audio stream handling
- `numpy` for numerical operations
- `scipy` for scientific computations
- `matplotlib.pyplot` for plotting (though not actively used in the current implementation)

The code initializes three microphones, each connected to a different input port, and sets up audio streams to read data from these microphones.

## Code Explanation

1. **Initialization**: 
   - The audio streams for three microphones are set up with a sample rate of 44.1 kHz and a buffer size (CHUNK) of 2048.
   - The microphones are instantiated using `pyaudio.PyAudio()`, and their streams are opened with specified parameters, including the input device index for each microphone.

2. **Signal Handling**:
   - A signal handler is defined to close the streams and terminate the program gracefully on receiving a SIGINT (Ctrl+C).

3. **Microphone Threads**:
   - Three separate threads are created for each microphone (MIC1, MIC2, MIC3). Each thread continuously reads data from its respective microphone.
   - The data is processed using Fast Fourier Transform (FFT) to convert the time-domain signal into the frequency domain.
   - The presence of a whistle is detected by checking if the FFT magnitude in a specific frequency range (1900 to 2000) exceeds a threshold (8,000,000).

4. **Whistle Detection**:
   - If a whistle is detected by any microphone, a corresponding flag (`whistle_flagP`, `whistle_flagQ`, or `whistle_flagR`) is set to `True`, and a message indicating the detection is printed.

5. **Main Processing Thread**:
   - A fourth thread (`mainProg`) runs concurrently, monitoring the whistle flags.
   - When a flag is set, the program prints the direction of the detected whistle based on which microphone detected the whistle:
     - Right (MIC1)
     - Left (MIC2)
     - Front (MIC3)
   - The flags are then reset to `False` for the next detection cycle.

## Execution

- The threads for the microphones and main processing are started and executed concurrently.
- The program continuously monitors and processes audio data, identifying the direction of any detected whistle sound.

## Conclusion

The implemented system successfully detects and localizes whistle sounds using three microphones and signal processing techniques. The use of threading ensures that audio data is processed in real-time, allowing for immediate detection and direction indication. This project demonstrates a practical application of audio signal processing and concurrent programming in Python.
