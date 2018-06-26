import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav

from util.speech import glottal_pulse, A_PARAMS, E_PARAMS, I_PARAMS, O_PARAMS, U_PARAMS, sintetize


def plot_sintetized_vowel(sintetized, glottal_pulse, fs, f0, letter, sample_periods=10):
    period_len = fs // f0
    samples = period_len * sample_periods
    sample_t = np.arange(samples) / fs

    plt.figure()
    plt.plot(sample_t, sintetized[:samples])
    plt.plot(sample_t, glottal_pulse[:samples])
    plt.legend(["Señal de '%s'" % letter, "Pulso glótico"])
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.title("'%s' sintetizada" % letter)
    plt.show()

    return  sintetized[:samples]


def spectral_analysis(sintetized, fs, f0, letter):
    period_len = fs // f0
    period = sintetized[:period_len]

    X = np.fft.fft(sintetized) / len(sintetized)
    freqs = np.arange(0, fs, fs / len(X))

    X_period = np.fft.fft(period) / len(period)

    plt.figure()
    plt.suptitle("Análisis en frecuencia de '%s' sintetizada" % letter)
    plt.subplot(2, 1, 1)
    plt.title("Espectro de amplitud")
    plt.plot(freqs, np.absolute(X))
    # plt.plot(period_freqs, np.absolute(X_period), linestyle='dashed')
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("|X(ω)|")
    # plt.legend(["Espectro de '%s' sintetizada" % letter, "Espectro de un periodo de '%s'" % letter])

    plt.subplot(2, 1, 2)
    plt.title("Espectrograma")
    length_window = period_len * 10

    plt.specgram(sintetized, NFFT=length_window, Fs=fs, noverlap=length_window // 2)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frecencia [Hz]")
    plt.subplots_adjust(hspace=0.5)

    plt.show()


def exercise(glottal_pulse, fs, f0, vowel_params, letter):
    sintetized = sintetize(glottal_pulse, fs, vowel_params)
    plot_sintetized_vowel(sintetized, glottal_pulse, fs, f0, letter)
    spectral_analysis(sintetized, fs, f0, letter)
    wav.write("../data/ex8/%s_sint2.wav" % letter, fs, sintetized)

if __name__ == "__main__":
    fs = 16000
    f0 = 200
    glot, _ = glottal_pulse(f0, Tp_pct=0.4, Tn_pct=0.16, P0=1, periods=200, fs=fs)

    exercise(glot, fs, f0, A_PARAMS, 'A')
    # exercise(glot, fs, f0, E_PARAMS, 'E')
    # exercise(glot, fs, f0, I_PARAMS, 'I')
    # exercise(glot, fs, f0, O_PARAMS, 'O')
    # exercise(glot, fs, f0, U_PARAMS, 'U')


