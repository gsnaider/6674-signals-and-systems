from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

from util.input import letters

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")
    t = np.arange(0, len(x) / fs, 1 / fs)
    plt.plot(t, x)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal x")
    for letter in letters:
        offset = 0.025
        letter_x = (letter.start + letter.end) / 2 - offset
        letter_y = 20000
        plt.text(letter_x, letter_y, letter.char, fontsize=12)
        plt.axvline(x=letter.start, color='r', linestyle='dashed')
        plt.axvline(x=letter.end, color='r', linestyle='dashed')
    plt.show()
