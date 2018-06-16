from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

class Letter:
    def __init__(self, char, start, end):
        self.char = char
        self.start = start
        self.end = end

letters = [
    Letter('C', 0.5544, 0.5786),
    Letter('O', 0.5786, 0.6646),
    Letter('N', 0.6646, 0.866),
    Letter('T', 0.9216, 0.9416),
    Letter('A', 0.9416, 1.0492),
    Letter('G', 1.0492, 1.2076),
    Letter('I', 1.2076, 1.2812),
    Letter('A', 1.2812, 1.3712),
    Letter('E', 1.3712, 1.4812),
    Letter('N', 1.4812, 1.5524),
    Letter('E', 1.5524, 1.6468),
    Letter('R', 1.676, 1.7600),
    Letter('G', 1.7600, 1.9080),
    Letter('I', 1.9080, 2.0600),
    Letter('A', 2.0600, 2.17),
    Letter('Y', 2.17, 2.2924),
    Letter('F', 2.2924, 2.448),
    Letter('E', 2.448, 2.5456),
    Letter('R', 2.5456, 2.711),
    Letter('V', 2.711, 2.7931),
    Letter('O', 2.7931, 2.9450),
    Letter('R', 2.9450, 3.1292)
]

if __name__ == "__main__":
    (fs, y) = wav.read("../data/hh15.WAV")
    t = np.arange(0, len(y) / fs, 1 / fs)
    plt.plot(t, y)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal x")
    for letter in letters:
        offset = 0.015
        x = (letter.start + letter.end) / 2 - offset
        y = 20000
        plt.text(x ,y, letter.char, fontsize=12)
        plt.axvline(x=letter.start, color='r', linestyle='dashed')
        plt.axvline(x=letter.end, color='r', linestyle='dashed')
    plt.show()