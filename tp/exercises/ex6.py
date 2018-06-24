import matplotlib.pyplot as plt
import numpy as np

from util.speech import glottal_pulse

if __name__ == "__main__":
    fs = 16000
    x, t = glottal_pulse(f0=200, Tp_pct=0.4, Tn_pct=0.16, P0=1, periods=10, fs=fs)

    plt.figure()
    plt.plot(t,x)
    plt.grid(linestyle='dashed')
    plt.title("Pulso Glótico")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.show()

    amplitude_spectrum = abs(np.fft.fft(x) / len(x))
    freqs = np.arange(0, fs/2, (fs/2) / len(amplitude_spectrum))

    plt.figure()
    plt.title("Espectro de amplitud de tren de pulsos")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Amplitud")
    plt.plot(freqs, amplitude_spectrum)
    plt.show()

    # Comparamos el espectro de un pulso con el del tren de pulsos
    pulse = x[:len(x) // 10]
    pulse_amp_spec = abs(np.fft.fft(pulse) / len(pulse))
    pulse_freqs = np.arange(0, fs / 2, (fs / 2) / len(pulse_amp_spec))

    plt.figure()
    plt.plot(freqs, amplitude_spectrum)
    plt.plot(pulse_freqs, pulse_amp_spec)
    plt.title("Espectros de amplitud")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Amplitud")
    plt.legend(["Espectro de amplitud del tren de pulsos", "Espectro de amplitud de un puslo"])
    plt.show()