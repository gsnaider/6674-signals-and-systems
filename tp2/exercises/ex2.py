from scipy.io import wavfile as wav
import numpy as np

from util.input import A_PERIOD_START, A_PERIOD_END, O_PERIOD_START, O_PERIOD_END, I_PERIOD_START, I_PERIOD_END
from util.signal import sub_signal, plot_period, plot_fourier_coefficients

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")

    x_a, t_a = sub_signal(x, fs, A_PERIOD_START, A_PERIOD_END)
    plot_period(x_a, t_a, 'A')
    X_a = np.fft.fft(x_a) / len(x_a)
    plot_fourier_coefficients(X_a, "Coeficientes de Fourier de periodo de 'A'")

    # TODO hacer otros periodos de la misma 'A'


    ## Periodos de otras letras para comparar

    x_o, t_o = sub_signal(x, fs, O_PERIOD_START, O_PERIOD_END)
    plot_period(x_o, t_o, 'O')
    X_o = np.fft.fft(x_o) / len(x_o)
    plot_fourier_coefficients(X_o, "Coeficientes de Fourier de periodo de 'O'")

    x_i, t_i = sub_signal(x, fs, I_PERIOD_START, I_PERIOD_END)
    plot_period(x_i, t_i, 'I')
    X_i = np.fft.fft(x_i) / len(x_i)
    plot_fourier_coefficients(X_i, "Coeficientes de Fourier de periodo de 'I'")
