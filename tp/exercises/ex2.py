from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
from exercises.ex1 import letters


if __name__ == "__main__":
    # Segunda 'A' de contagia
    (fs, y) = wav.read("../data/hh15.WAV")
    t = np.arange(0, len(y) / fs, 1 / fs)
    period_start = 1.30657
    period_end = 1.313
    T = period_end - period_start
    x = y[int(period_start * fs): int(period_end * fs)]
    t = np.arange(0, len(x) / fs, 1 / fs)
    # plt.plot(t, x)

    # Tomamos transformada de Fourier
    X = np.fft.fft(x)
    mod = np.absolute(X)
    plt.stem(mod)