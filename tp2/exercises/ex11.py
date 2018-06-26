import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav

from util.input import fundamental_freqs, sonorous_segments
from util.signal import PSOLA


def plot_in_time(t, x, new_x_09, new_x_08, new_x_07, new_x_11, new_x_12, new_x_13):
    plt.figure()
    plt.subplot(4, 1, 1)
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

    plt.figure()
    plt.subplot(4, 1, 1)
    plt.title("Señal original")
    plt.plot(t, x)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplot(4, 1, 2)
    plt.title("Señal con f0 en 110%")
    plt.plot(t, new_x_11)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplot(4, 1, 3)
    plt.title("Señal con f0 en 120%")
    plt.plot(t, new_x_12)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplot(4, 1, 4)
    plt.title("Señal con f0 en 130%")
    plt.plot(t, new_x_13)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplots_adjust(hspace=0.7)

    plt.show()


def plot_new_x(x, fs, f0s, new_x, new_f0_pct):
    t = np.arange(0, len(x) / fs, 1 / fs)

    new_f0s = fundamental_freqs(new_x, fs)

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.suptitle("Señal con f0 en %d%%" % (new_f0_pct * 100), fontsize=16)
    plt.title("Señal de audio")
    plt.plot(t, new_x)
    plt.plot(t, x, alpha=0.6)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.legend(["Señal original", "Señal con f0 en %d%%" % (new_f0_pct * 100)])

    plt.subplot(2, 1, 2)
    plt.plot(t, f0s)
    plt.plot(t, new_f0s)
    plt.grid(linestyle='dashed')
    plt.title("Frequencia fundamental")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frequencia [Hz]")
    plt.legend(["Señal original", "Señal con f0 en %d%%" % (new_f0_pct * 100)])

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def exercise(x, fs, sonorous_segs, f0s, new_f0_pct, plot=False):
    new_x = PSOLA(x, fs, sonorous_segs, f0s, new_f0_pct, plot)
    plot_new_x(x, fs, f0s, new_x, new_f0_pct)
    wav.write("../data/hh15_f0_%d.wav" % (new_f0_pct * 100), fs, new_x)

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")

    f0s = fundamental_freqs(x, fs)

    sonorous_segs = sonorous_segments()

    exercise(x, fs, sonorous_segs, f0s, 0.9)
    exercise(x, fs, sonorous_segs, f0s, 0.8)
    exercise(x, fs, sonorous_segs, f0s, 0.7)
    exercise(x, fs, sonorous_segs, f0s, 1.1)
    exercise(x, fs, sonorous_segs, f0s, 1.2)
    exercise(x, fs, sonorous_segs, f0s, 1.3)