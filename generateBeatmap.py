import aubio

def generateBeatmap(path, method, outPath, threshold):
    win_s = 512                 # fft size
    hop_s = win_s // 2 
    #path = "crab_rave.wav"
    s = aubio.source(path)
    samplerate = s.samplerate

    o = aubio.onset(method)
    o.set_threshold(threshold)

    # list of onsets, in samples
    timestamps = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        if o(samples):
            #print("%f" % o.get_last_s())
            timestamps.append(o.get_last())
        total_frames += read
        if read < hop_s: break

    f= open("beatmaps/" + outPath, "w+")
    for timestamp in timestamps:
        f.write(str(timestamp / samplerate*1.0) + "\n")
    f.close()
    print("Done with " + method)



#methods = ["energy", "hfc", "complex", "phase", "wphase", "specdiff", "kl", "mkl", "specflux"]

#for method in methods:
#    generateBeatmap(method)
