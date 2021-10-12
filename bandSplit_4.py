from scipy.io import wavfile
from scipy import signal
import numpy

from pydub import AudioSegment

# Specify the 3 frequency thresholds which will be used to create 4 bands
intervals = [800, 1600, 4000]

def bandSplit(path):
    monoFile = AudioSegment.from_wav(path)
    monoFile = monoFile.set_channels(1)
    monoFile.export("mono_file.wav", format="wav")

    # First band

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=intervals[0], fs=sr, pass_zero="lowpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_band1.wav", sr, x.astype(numpy.int16))

    # Second band

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=[intervals[0], intervals[1]], fs=sr, pass_zero="bandpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_band2.wav", sr, x.astype(numpy.int16))

    # Third band

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=[intervals[1], intervals[2]], fs=sr, pass_zero="bandpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_band3.wav", sr, x.astype(numpy.int16))

    # Fourth

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=intervals[2], fs=sr, pass_zero="highpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_band4.wav", sr, x.astype(numpy.int16))
