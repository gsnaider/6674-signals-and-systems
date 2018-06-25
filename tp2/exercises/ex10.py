import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav

from util.input import setup_input_signal_plot, fundamental_freqs

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")
    t = np.arange(0, len(x) / fs, 1 / fs)

    f0s = fundamental_freqs(x, fs)

    plt.figure()
    plt.subplot(2,1,1)
    setup_input_signal_plot(t, x)

    plt.subplot(2, 1, 2)
    plt.plot(t, f0s)
    plt.grid(linestyle='dashed')
    plt.title("Frequencia fundamental")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frequencia [Hz]")

    plt.show()