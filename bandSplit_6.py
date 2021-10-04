from scipy.io import wavfile
from scipy import signal
import numpy

from pydub import AudioSegment

# Specify the 5 frequency thresholds which will be used to create 6 bands
intervals = [250, 800, 2500, 4000, 5000]

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

    # Fourth band

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=[intervals[2], intervals[3]], fs=sr, pass_zero="bandpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_band4.wav", sr, x.astype(numpy.int16))

    # Fifth band

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=[intervals[3], intervals[4]], fs=sr, pass_zero="bandpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_band5.wav", sr, x.astype(numpy.int16))

    # Sixth band

    sr, x = wavfile.read("mono_file.wav")

    b = signal.firwin(101, cutoff=intervals[4], fs=sr, pass_zero="highpass")
    x = signal.lfilter(b, [1.0], x)
    wavfile.write("music_band6.wav", sr, x.astype(numpy.int16))
