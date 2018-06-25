import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav

from util.input import fundamental_freqs, sonorous_segments
from util.signal import PSOLA

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")
    t = np.arange(0, len(x) / fs, 1 / fs)

    f0s = fundamental_freqs(x, fs)

    sonorous_segs = sonorous_segments()

    new_f0_pct = 0.9
    PSOLA(x, fs, sonorous_segs, f0s, new_f0_pct)