import numpy as np

from util.signal import cepstrum
import matplotlib.pyplot as plt
from util.speech import glottal_pulse, A_PARAMS, sintetize, U_PARAMS, E_PARAMS, I_PARAMS, O_PARAMS


def exercise(glottal_pulse, fs, f0, vowel_params, letter):
    a_sintetized = sintetize(glottal_pulse, fs, vowel_params)

    sample_periods = 10
    period_len = fs // f0
    samples = period_len * sample_periods
    t_sample = np.arange(samples) / fs
    a_sint_sample = a_sintetized[:samples]

    ceps = cepstrum(a_sint_sample)

    x_range_start = int(1 / 500 * fs)
    x_range_end = int(1 / 50 * fs)

    max_x = np.argmax(np.real(ceps[x_range_start: x_range_end]))
    max_cep = np.max(np.real(ceps[x_range_start: x_range_end]))

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.title("'%s' sintetizada" % letter)
    plt.plot(t_sample, a_sint_sample)
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




if __name__ == "__main__":
    fs = 16000
    f0 = 200
    glot, _ = glottal_pulse(f0, Tp_pct=0.4, Tn_pct=0.16, P0=250, periods=200, fs=fs)

    exercise(glot, fs, f0, A_PARAMS, 'A')
    exercise(glot, fs, f0, E_PARAMS, 'E')
    exercise(glot, fs, f0, I_PARAMS, 'I')
    exercise(glot, fs, f0, O_PARAMS, 'O')
    exercise(glot, fs, f0, U_PARAMS, 'U')



