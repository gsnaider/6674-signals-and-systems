import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav

from util.signal import PSOLA
from util.speech import glottal_pulse, sintetize, A_PARAMS, E_PARAMS, I_PARAMS, O_PARAMS, U_PARAMS


def plot_new_x(x, fs, new_x, new_f0_pct, letter):
    t = np.arange(0, len(x) / fs, 1 / fs)
    new_period_len = fs // (f0 * new_f0_pct)

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.suptitle("Señal de '%s'" % letter, fontsize=16)
    plt.title("Señal de audio")
    plt.plot(t[100:800], x[100:800], alpha=0.6)
    plt.plot(t[100:800], new_x[100:800])
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.legend(["Señal original", "Señal con f0 en %d%%" % (new_f0_pct * 100)])

    plt.subplot(2, 1, 2)
    plt.title("Espectrograma de nueva señal")
    length_window = int(new_period_len * 10)

    plt.specgram(new_x, NFFT=length_window, Fs=fs, noverlap=length_window // 2)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frecencia [Hz]")
    plt.subplots_adjust(hspace=0.5)

    plt.subplots_adjust(hspace=0.5)
    plt.show()

def exercise(glottal_pulse, t, fs, f0, new_f0_pct, vowel_params, letter, plot=False):
    x = sintetize(glottal_pulse, fs, vowel_params)

    sonorous_segs = [(t[0], t[-1])]
    f0s = np.repeat(f0, len(t))
    new_x = PSOLA(x, fs, sonorous_segs, f0s, new_f0_pct, plot)

    plot_new_x(x, fs, new_x, new_f0_pct, letter)
    wav.write("../data/ex14/%s_f0_%d.wav" % (letter, new_f0_pct * 100), fs, new_x)

if __name__ == "__main__":
    fs = 16000
    f0 = 200
    glot, t = glottal_pulse(f0, Tp_pct=0.4, Tn_pct=0.16, P0=1, periods=200, fs=fs)

    exercise(glot, t, fs, f0, 0.5, A_PARAMS, 'A')
    exercise(glot, t, fs, f0, 0.5, E_PARAMS, 'E')
    exercise(glot, t, fs, f0, 0.5, I_PARAMS, 'I')
    exercise(glot, t, fs, f0, 0.5, O_PARAMS, 'O')
    exercise(glot, t, fs, f0, 0.5, U_PARAMS, 'U')
