import numpy as np
import matplotlib.pyplot as plt


def sub_signal(x, fs, start, end):
    sub_x = x[int(start * fs): int(end * fs)]
    sub_t = np.arange(0, len(sub_x) / fs, 1 / fs) + start
    return sub_x, sub_t


def plot_fourier_coefficients(X, plot_title):
    plt.figure()
    plt.suptitle(plot_title, fontsize=16)

    plt.subplot(2, 1, 1)
    plt.title("Módulo")
    plt.xlabel('k')
    plt.ylabel('|ak|')
    plt.grid(linestyle='dashed')
    plt.stem(np.absolute(X))

    plt.subplot(2, 1, 2)
    plt.title("Fase")
    plt.xlabel('k')
    plt.ylabel('< ak')
    plt.grid(linestyle='dashed')
    plt.stem(np.angle(X))

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def plot_period(x, t, name):
    start = x[0]
    end = x[len(x) - 1]
    print('Period start value:\t', start)
    print('Period end value:\t', end)
    print('Difference:\t', abs(end - start))

    plt.figure()
    plt.grid(linestyle='dashed')
    plt.title("Periodo de '%s'" % name)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Señal')
    plt.plot(t, x)
    plt.show()


def plot_specgram(x, fs, length_window, name):
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.suptitle('Señal y Espectrograma de %s' % name, fontsize=16)

    t = np.arange(0, len(x) / fs, 1 / fs)
    plt.grid(linestyle='dashed')
    plt.plot(t, x)
    plt.title("Señal")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplot(2, 1, 2)
    plt.specgram(x, NFFT=length_window, Fs=fs, noverlap=length_window // 2)
    plt.title("Espectrograma")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frecencia [Hz]")

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def glottal_pulse(f0, Tp_pct, Tn_pct, P0, periods, fs):
    pulse_length = fs // f0
    t = np.arange(0, periods / f0, 1 / fs)
    x = np.zeros(pulse_length)

    Tp_idx = int(pulse_length * Tp_pct) + 1
    Tp = t[Tp_idx]

    Tn_idx = int(pulse_length * Tn_pct) + 1
    Tn = t[Tn_idx]

    x[:Tp_idx] = P0 / 2 * (1 - np.cos(t[:Tp_idx] / Tp * np.pi))
    x[Tp_idx:Tp_idx + Tn_idx] = P0 * np.cos((t[Tp_idx:Tp_idx + Tn_idx] - Tp) / Tn * np.pi / 2)

    return np.squeeze(np.tile(x, [1, periods])), t


def Hn(z, Fn, Fs, B):
    p_n = pn(Fn, Fs, B)
    return 1 / ((1 - p_n * 1 / z) * (1 - np.conj(p_n) * 1 / z)), [p_n, np.conj(p_n)]


def pn(Fn, Fs, B):
    return np.exp(-2 * np.pi * B / Fs) * np.exp(1j * 2 * np.pi * Fn / Fs)
