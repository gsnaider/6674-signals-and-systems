from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

from util.input import letters, setup_input_signal_plot

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")
    t = np.arange(0, len(x) / fs, 1 / fs)
    setup_input_signal_plot(t, x)
    plt.show()