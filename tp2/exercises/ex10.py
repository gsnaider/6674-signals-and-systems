import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav

from util.input import letters
from util.speech import fundamental_freq

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")
    t = np.arange(0, len(x) / fs, 1 / fs)

    window_time = 0.05
    window_size = int(window_time * fs)
    print("Tamaño de ventana de tiempo: %fs" % (window_time))

    n_segments = len(x) // window_size

    segments = np.array_split(x, n_segments)
    f0s = []
    for segment in segments:
        if np.max(np.abs(segment)) > 200:
            f0s.append(fundamental_freq(segment, fs))
        else:
            f0s.append(0)

    f0s = np.array(f0s)
    f0s = np.repeat(f0s, window_size)

    # Padding al final de f0s para que coincida con len(t)
    f0s = np.pad(f0s, (0, len(t) - len(f0s)), 'edge')


    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(t,x)
    plt.grid(linestyle='dashed')
    plt.title("Señal de voz")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal x")
    for letter in letters:
        offset = 0.015
        letter_x = (letter.start + letter.end) / 2 - offset
        letter_y = 20000
        plt.text(letter_x, letter_y, letter.char, fontsize=12)
        plt.axvline(x=letter.start, color='r', linestyle='dotted')
        plt.axvline(x=letter.end, color='r', linestyle='dotted')


    plt.subplot(2, 1, 2)
    plt.plot(t, f0s)
    plt.grid(linestyle='dashed')
    plt.title("Frequencia fundamental")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frequencia [Hz]")

    plt.show()