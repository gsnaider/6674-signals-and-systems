import numpy as np
from scipy.signal import lfilter

from util.signal import cepstrum

A_PARAMS = [
    (830, 110),
    (1400, 160),
    (2890, 210),
    (3930, 230)
]

E_PARAMS = [
    (500, 80),
    (2000, 156),
    (3130, 190),
    (4150, 220)
]

I_PARAMS = [
    (330, 70),
    (2765, 130),
    (3740, 178),
    (4366, 200)
]
O_PARAMS = [
    (546, 97),
    (934, 130),
    (2966, 185),
    (3930, 240)
]

U_PARAMS = [
    (382, 74),
    (740, 150),
    (2760, 210),
    (3380, 180)
]

def Hn(z, Fn, Fs, B):
    p_n = pn(Fn, Fs, B)
    return 1 / ((1 - p_n * 1 / z) * (1 - np.conj(p_n) * 1 / z)), [p_n, np.conj(p_n)]


def pn(Fn, Fs, B):
    return np.exp(-2 * np.pi * B / Fs) * np.exp(1j * 2 * np.pi * Fn / Fs)


def vocal_tract_model(params, Fs):
    H = 1
    w = np.arange(0, np.pi, 0.001)
    poles = []
    zeros = []
    Hs = []
    for Fn, B in params:
        H_n, H_n_poles = Hn(np.exp(1j * w), Fn, Fs, B)
        H *= H_n
        Hs.append(H_n)
        poles.append(H_n_poles)

    poles = np.array(poles).flatten()
    zeros = np.array(zeros).flatten()

    freqs = np.arange(0,Fs/2,(Fs/2)/len(H))
    return H, freqs, Hs, poles, zeros


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

    glot = np.squeeze(np.tile(x, [1, periods]))
    glot = glot - np.mean(glot)

    return glot, t




def sintetize(glottal_pulse, fs, vowel_params):
    H, w, Hs, poles, zeros = vocal_tract_model(vowel_params, fs)
    den_coefs = np.poly(poles)

    sintetized = lfilter([1], den_coefs, glottal_pulse)
    return sintetized


def fundamental_freq(x, fs):
    ceps = cepstrum(x)

    x_range_start = int(1 / 500 * fs)
    x_range_end = int(1 / 50 * fs)

    max_x = np.argmax(np.real(ceps[x_range_start: x_range_end]))

    max_t = (x_range_start + max_x) / fs
    f0 = 1 / max_t

    return f0