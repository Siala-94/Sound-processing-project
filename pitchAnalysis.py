import sys
import aubio

def generatePitches(path, outPath):

    downsample = 1
    samplerate = 44100 // downsample

    win_s = 4096 // downsample # fft size
    hop_s = 512 // downsample # hop size

    s = aubio.source(path, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]

        confidence = pitch_o.get_confidence()

        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    f = open("pitchmaps/" + outPath, "w+")
    for p in pitches:
        f.write(str(p) + "\n")
    f.close()

    print("Done. Total frames = " + str(total_frames))
