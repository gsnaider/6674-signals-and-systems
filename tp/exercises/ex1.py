from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    (fs, y) = wav.read("../data/hh15.WAV")
    t = np.arange(0, len(y)/fs,  1/fs)
    plt.plot(t,y)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal x")
    plt.figtext(0.5, 20000, "Contagia energía y fervor", fontsize=12)
    plt.show()
