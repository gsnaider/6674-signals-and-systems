import numpy as np


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

    poles = np.array(poles)
    zeros = np.array(zeros)

    return H, w, Hs, poles, zeros


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


