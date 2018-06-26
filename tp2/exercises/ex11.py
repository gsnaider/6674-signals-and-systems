import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav

from util.input import fundamental_freqs, sonorous_segments, setup_input_signal_plot
from util.signal import PSOLA

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")
    t = np.arange(0, len(x) / fs, 1 / fs)

    f0s = fundamental_freqs(x, fs)

    sonorous_segs = sonorous_segments()

    new_x_09 = PSOLA(x, fs, sonorous_segs, f0s, 0.9, plot=True)
    new_x_08 = PSOLA(x, fs, sonorous_segs, f0s, 0.8)
    new_x_07 = PSOLA(x, fs, sonorous_segs, f0s, 0.7)

    plt.figure()
    plt.subplot(4,1,1)
    plt.title("Señal original")
    plt.plot(t, x)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplot(4, 1, 2)
    plt.title("Señal con f0 en 90%")
    plt.plot(t, new_x_09)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplot(4, 1, 3)
    plt.title("Señal con f0 en 80%")
    plt.plot(t, new_x_08)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplot(4, 1, 4)
    plt.title("Señal con f0 en 70%")
    plt.plot(t, new_x_07)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplots_adjust(hspace=0.7)

    plt.show()

    wav.write("../data/hh15_09.wav", fs, new_x_09)
    wav.write("../data/hh15_08.wav", fs, new_x_08)
    wav.write("../data/hh15_07.wav", fs, new_x_07)