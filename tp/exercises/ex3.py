import numpy as np
import matplotlib.pyplot as plt

from scipy.io import wavfile as wav

from util.input import A_PERIOD_START, A_PERIOD_END, I_PERIOD_START, I_PERIOD_END, O_PERIOD_START, O_PERIOD_END
from util.signal import sub_signal, plot_fourier_coefficients


def fourier_and_rebuild(x, fs, letter, start, end, threshold=None):
    x_sub, _ = sub_signal(x, fs, start, end)

    # Calculamos los coeficientes de Fourier
    X = np.fft.fft(x_sub) / len(x_sub)

    if (threshold != None):
        # Pasamos a cero los coeficientes menores al umbral
        X[np.absolute(X) < threshold] = 0
        plot_fourier_coefficients(X, "Coeficientes de Fourier truncados de periodo de '%s'" % letter)

    # Reconstruimos la señal a partir de sus coeficientes
    x_rebuilt = np.real(np.fft.ifft(X))

    # Periodizamos la señal reconstruida y la guardamos como un audio
    x_periodic = np.squeeze(np.tile(x_rebuilt, [1, 500]))

    return x_rebuilt, x_periodic


def exercise(x, fs, letter, period_start, period_end, threshold):
    x_period, x_periodic = fourier_and_rebuild(x, fs, letter, period_start, period_end)
    x2_period, x2_periodic = fourier_and_rebuild(x, fs, letter, period_start, period_end, threshold)

    # Graficamos las señales reconstruidas
    plt.figure()
    plt.grid(linestyle='dashed')
    plt.title("Periodos de '%s' reconstruidos" % letter)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")
    t = np.arange(len(x_period)) / fs
    plt.plot(t, x_period)
    plt.plot(t, x2_period)
    plt.legend(["'%s' con coeficientes originales" % letter, "'%s' con coeficientes truncados" % letter])
    plt.show()

    plt.figure()
    plt.grid(linestyle='dashed')
    plt.title("Señales de '%s' periodizadas" % letter)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")
    periods = 4
    samples = len(x_period) * periods
    t = np.arange(samples) / fs
    plt.plot(t, x_periodic[:samples])
    plt.plot(t, x2_periodic[:samples])
    plt.legend(["'%s' con coeficientes originales" % letter, "'%s' con coeficientes truncados" % letter])
    plt.show()

    output1 = "../data/%s1.wav" % letter
    output2 = "../data/%s2.wav" % letter
    wav.write(output1, fs, x_periodic)
    wav.write(output2, fs, x2_periodic)


if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")

    exercise(x, fs, 'A', A_PERIOD_START, A_PERIOD_END, threshold=50)
    # exercise(x, fs, 'O', O_PERIOD_START, O_PERIOD_END, threshold=250)
    # exercise(x, fs, 'I', I_PERIOD_START, I_PERIOD_END, threshold=200)