import numpy as np

from util.signal import cepstrum
import matplotlib.pyplot as plt
from util.speech import glottal_pulse, A_PARAMS, sintetize, U_PARAMS, E_PARAMS, I_PARAMS, O_PARAMS, vocal_tract_model

FREQ_TRESHOLDS = {'A': 457, 'E': 400, 'I': 267, 'O': 320, 'U': 533}

def cepstrum_analysis(fs, sintetized, letter):
    t = np.arange(len(sintetized)) / fs

    ceps = cepstrum(sintetized)

    x_range_start = int(1 / 500 * fs)
    x_range_end = int(1 / 150 * fs)

    max_x = np.argmax(np.real(ceps[x_range_start: x_range_end]))
    max_cep = np.max(np.real(ceps[x_range_start: x_range_end]))

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.title("'%s' sintetizada" % letter)
    plt.plot(t, sintetized)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")

    plt.subplot(2, 1, 2)
    plt.title("Cepstrum de '%s'" % letter)
    plt.plot(t, np.real(ceps))
    plt.grid(linestyle='dashed')
    plt.xlabel("Quefrencia [s]")
    plt.ylabel("Re{c[n]}")
    plt.axvline(x=1 / 150, color='r', linestyle='dotted')
    plt.axvline(x=1 / 500, color='r', linestyle='dotted')

    max_t = (x_range_start + max_x) / fs
    f0 = 1 / max_t
    max_text = "max(c[n]) = %f\nQuefrencia = %fs\nf0 = %fHz" % (max_cep, max_t, f0)
    plt.text(max_t + 0.0001, max_cep + 0.05, max_text, fontsize=10)
    plt.axvline(x=max_t, color='b', linestyle='dotted')

    plt.show()

    print("INFO DE '%s'" % letter)
    print("max{c[n]} = %f" % max_cep)
    print("Q0 = %f" % max_t)
    print("f0 = %f" % f0)
    print()

    return ceps


def estimate_freq_response(fs, ceps, vowel_params, letter):
    freq_threshold = FREQ_TRESHOLDS[letter]
    quef_threshold = 1 / freq_threshold
    x_threshold = int(quef_threshold * fs)

    ceps_trunc = np.copy(ceps)
    ceps_trunc[x_threshold:] = 0
    t = np.arange(len(ceps)) / fs

    plt.figure()
    plt.title("Cepstrum de '%s'" % letter)
    plt.grid(linestyle='dashed')
    plt.plot(t, np.real(ceps))
    plt.plot(t, np.real(ceps_trunc))
    plt.axvline(x=t[x_threshold], color='red', linestyle='dashed')
    plt.text(t[x_threshold], 1, "Umbral: %f" % t[x_threshold])
    plt.legend(["Cepstrum", "Cepstrum truncado"])
    plt.xlabel("Quefrencia [s]")
    plt.ylabel("Re{c[n]}")
    plt.show()


    H_estimated = np.exp(np.real(np.fft.rfft(ceps_trunc)))
    H_estimated = np.abs(H_estimated)

    H, freqs, _, _, _ = vocal_tract_model(vowel_params, fs)
    H = np.abs(H)
    H = H[::int(len(H) / len(H_estimated))][:len(H_estimated)]
    freqs = freqs[::int(len(freqs) / len(H_estimated))][:len(H_estimated)]

    # TODO aca normalizo para que coincidan, ver si hay otra forma
    H_estimated = H_estimated / max(H_estimated)
    H = H / max(H)

    plt.figure()
    plt.title("Comparación de respuesta en frecuencia de '%s'" % letter)
    plt.plot(freqs, H)
    plt.plot(freqs, H_estimated)
    plt.xlabel("Frecuencia[Hz]")
    plt.ylabel("|H(ω)|")
    plt.legend(["H", "H estimada"])
    plt.show()


def exercise(glottal_pulse, fs, vowel_params, letter):
    sintetized = sintetize(glottal_pulse, fs, vowel_params)
    ceps = cepstrum_analysis(fs, sintetized, letter)
    estimate_freq_response(fs, ceps, vowel_params, letter)



if __name__ == "__main__":
    fs = 16000
    f0 = 200
    glot, t = glottal_pulse(f0, Tp_pct=0.4, Tn_pct=0.16, P0=1, periods=10, fs=fs)

    glot = glot - np.mean(glot)
    plt.figure()
    plt.grid(linestyle='dashed')
    plt.title("Pulso Glótico normalizado")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.plot(t, glot)
    plt.show()

    # exercise(glot, fs, A_PARAMS, 'A')
    exercise(glot, fs, E_PARAMS, 'E')
    # exercise(glot, fs, I_PARAMS, 'I')
    # exercise(glot, fs, O_PARAMS, 'O')
    # exercise(glot, fs, U_PARAMS, 'U')



