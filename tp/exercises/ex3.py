import numpy as np
import matplotlib.pyplot as plt

from scipy.io import wavfile as wav

from util.input import A_PERIOD_START, A_PERIOD_END, I_PERIOD_START, I_PERIOD_END
from util.signal import sub_signal, plot_fourier_coefficients


def exercise(x, fs, output, threshold=None):

    # Obtenemos un periodo de una 'A'
    x_a, _ = sub_signal(x, fs, A_PERIOD_START, A_PERIOD_END)

    # Calculamos los coeficientes de Fourier
    X_a = np.fft.fft(x_a) / len(x_a)

    if (threshold != None):
        # Pasamos a cero los coeficientes menores al umbral
        X_a[np.absolute(X_a) < threshold] = 0
        plot_fourier_coefficients(X_a, "Coeficientes de Fourier truncados de periodo de 'A'")

    # Reconstruimos la señal a partir de sus coeficientes
    x_a_rebuilt = np.real(np.fft.ifft(X_a))

    # Periodizamos la señal reconstruida y la guardamos como un audio
    x_a_periodic = np.squeeze(np.tile(x_a_rebuilt, [1, 500]))
    wav.write(output, fs, x_a_periodic)

    return x_a_rebuilt, x_a_periodic

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")

    x_a, x_a_periodic = exercise(x,fs,"../data/A1.wav")
    x_a2, x_a2_periodic = exercise(x, fs,"../data/A2.wav", threshold=100)


    # Graficamos las señales reconstruidas
    plt.figure()
    plt.grid(linestyle='dashed')
    plt.title("Periodos de 'A' reconstruidos")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")
    t = np.arange(len(x_a)) / fs
    plt.plot(t, x_a)
    plt.plot(t, x_a2)
    plt.legend(["'A' con coeficientes originales","'A' con coeficientes truncados"])
    plt.show()


    plt.figure()
    plt.grid(linestyle='dashed')
    plt.title("Señales de 'A' periodizadas")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    periods = 4
    samples = len(x_a) * periods
    t = np.arange(samples) / fs
    plt.plot(t, x_a_periodic[:samples])
    plt.plot(t, x_a2_periodic[:samples])

    plt.legend(["'A' con coeficientes originales", "'A' con coeficientes truncados"])
    plt.show()