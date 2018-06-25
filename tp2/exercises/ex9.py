import numpy as np

from util.signal import cepstrum
import matplotlib.pyplot as plt
from util.speech import glottal_pulse, A_PARAMS, sintetize, U_PARAMS, E_PARAMS, I_PARAMS, O_PARAMS, vocal_tract_model


def cepstrum_analysis(fs, f0, sintetized, letter):
    sample_periods = 10
    period_len = fs // f0
    samples = period_len * sample_periods
    t_sample = np.arange(samples) / fs
    sint_sample = sintetized[:samples]

    ceps = cepstrum(sint_sample)

    x_range_start = int(1 / 500 * fs)
    x_range_end = int(1 / 50 * fs)

    max_x = np.argmax(np.real(ceps[x_range_start: x_range_end]))
    max_cep = np.max(np.real(ceps[x_range_start: x_range_end]))

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.title("'%s' sintetizada" % letter)
    plt.plot(t_sample, sint_sample)
    plt.grid(linestyle='dashed')
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")

    plt.subplot(2, 1, 2)
    plt.title("Cepstrum de '%s'" % letter)
    plt.plot(t_sample, np.real(ceps))
    plt.grid(linestyle='dashed')
    plt.xlabel("Quefrencia [s]")
    plt.ylabel("Re{c[n]}")
    plt.axvline(x=1 / 50, color='r', linestyle='dotted')
    plt.axvline(x=1 / 500, color='r', linestyle='dotted')

    max_t = (x_range_start + max_x) / fs
    f0 = 1 / max_t
    max_text = "max(c[n]) = %f\nQuefrencia = %f\nf0 = %f" % (max_cep, max_t, f0)
    plt.text(max_t, max_cep + 0.05, max_text, fontsize=10)
    plt.axvline(x=max_t, color='b', linestyle='dotted')

    plt.show()

    print("INFO DE '%s'" % letter)
    print("max{c[n]} = %f" % max_cep)
    print("Q0 = %f" % max_t)
    print("f0 = %f" % f0)
    print()


def estimate_freq_response(fs, f0, sintetized, vowel_params, letter):
    ceps = cepstrum(sintetized)
    freq_threshold = 500

    quef_threshold = 1 / freq_threshold
    x_threshold = int(quef_threshold * fs)
    ceps[x_threshold:] = 0

    # t = np.arange(len(ceps)) / fs
    # plt.figure()
    # plt.plot(t, np.real(ceps))
    # plt.title("Cepstrum truncado de '%s'" % letter)
    # plt.grid(linestyle='dashed')
    # plt.xlabel("Quefrencia [s]")
    # plt.ylabel("Re{c[n]}")
    # plt.show()

    H_estimated = np.exp(np.fft.fft(ceps))
    H, w, Hs, poles, zeros = vocal_tract_model(vowel_params, fs)

    H_estimated = np.abs(H_estimated)
    H = np.abs(H)

    # TODO aca normalizo para q coincidan, ver si hay otra forma
    H_estimated = H_estimated / np.max(H_estimated)
    H = H / np.max(H)

    plt.figure()
    plt.title("Comparación de respuesta en frecuencia de '%s'" % letter)
    plt.plot(w, H)
    plt.plot(w, H_estimated[:len(w)])
    plt.xlabel("ω")
    plt.ylabel("|H(ω)|")
    plt.legend(["H", "H estimada"])
    plt.show()


def exercise(glottal_pulse, fs, f0, vowel_params, letter):
    sintetized = sintetize(glottal_pulse, fs, vowel_params)

    # cepstrum_analysis(fs, f0, sintetized, letter)
    estimate_freq_response(fs, f0, sintetized, vowel_params, letter)



if __name__ == "__main__":
    fs = 16000
    f0 = 200
    glot, _ = glottal_pulse(f0, Tp_pct=0.4, Tn_pct=0.16, P0=250, periods=200, fs=fs)

    exercise(glot, fs, f0, A_PARAMS, 'A')
    exercise(glot, fs, f0, E_PARAMS, 'E')
    exercise(glot, fs, f0, I_PARAMS, 'I')
    exercise(glot, fs, f0, O_PARAMS, 'O')
    exercise(glot, fs, f0, U_PARAMS, 'U')



