from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    (fs_orig, x_orig) = wav.read("../data/hh15.WAV")
    (fs_rec, x_rec) = wav.read("../data/recorded.wav")

    plt.subplot(2,1,1)
    plt.suptitle('Comparación de señal original y grabada', fontsize=16)

    t_orig = np.arange(0, len(x_orig) / fs_orig, 1 / fs_orig)
    plt.plot(t_orig, x_orig)
    plt.grid(linestyle='dashed')
    plt.title("Señal original")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplot(2, 1, 2)
    t_rec = np.arange(0, len(x_rec) / fs_rec, 1 / fs_rec)
    plt.plot(t_rec, x_rec)
    plt.grid(linestyle='dashed')
    plt.title("Señal grabada")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplots_adjust(hspace=0.5)
    plt.show()


