# Realtime FFT from any audio input with PyAudio and Matplotlib

What we want to achieve

https://user-images.githubusercontent.com/11285367/202855971-0a25c417-be3f-4ea4-920a-c94db6a97e20.mp4

you can select signal from any input source. It opens a Matplotlib window which displays FFT values of the input signal. 

# Prerequisites

## 1. Install Port Audio.

see [official portaudio website](http://www.portaudio.com/)

##### MacOS

```
brew install portaudio
``` 

##### Linux

```
sudo apt-get install python3-pyaudio
```

## 2. Install PyAudio

```
pip install pyaudio
```

see [official pyaudio website](https://people.csail.mit.edu/hubert/pyaudio/)


## 3. install further dependencies 

##### [inquirer](https://pypi.org/project/inquirer/)

```
pip install inquirer
```

##### [numpy](https://pypi.org/project/numpy/)

```
pip install inquirer
```

##### [matplotlib](https://pypi.org/project/matplotlib/)

```
pip install matplotlib
```

# Execute

to run the application start with 

```
python app.py
```

# Info

if you new to the topic FFT, i can recommend you watching [this video](https://youtu.be/spUNpyF58BY). It is nicely animated and explained :) 


