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