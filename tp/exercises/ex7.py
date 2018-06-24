import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

from util.signal import Hn


def plot_H(params, Fs, letter):
    H = 1
    w = np.arange(0, np.pi, 0.001)
    poles = []
    zeros = []
    plt.figure()
    plt.title("Respuesta en frecuencia de '%s'" % letter)
    for Fn, B in params:
        H_n, H_n_poles = Hn(np.exp(1j * w), Fn, Fs, B)
        H *= H_n
        plt.plot(w, abs(H_n), dashes=[6, 2])
        poles.append(H_n_poles)
    plt.plot(w, abs(H))
    plt.grid(linestyle='dashed')
    plt.title("Modelo de tracto vocal '%s'" % letter)

    # TODO checkear como pasar de ω a Hz
    plt.xlabel("ω")

    plt.ylabel("|H(ω)|")
    plt.legend(["H1", "H2", "H3", "H4", "H"])
    plt.show()
    plt.figure()

    poles = np.array(poles)
    zeros = np.array(zeros)

    ax = plt.subplot(1,1,1)
    plt.title("Polos y ceros de tracto vocal '%s'" % letter)
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.grid(linestyle='dashed')
    plt.axis([-2, 2, -2, 2])
    plt.scatter(np.real(poles), np.imag(poles), marker='x', color='red')
    plt.scatter(np.real(zeros), np.imag(zeros), marker='o', color='blue')
    plt.legend(["Polos", "Ceros"])
    plt.axvline(0, color = 'black')
    plt.axhline(0, color = 'black')
    ax.add_patch(patches.Circle((0,0), radius=1, fill=False, ls='dashed', color='black'))


    plt.show()


if __name__ == "__main__":
    Fs = 16000

    a_params = [
        (830, 110),
        (1400, 160),
        (2890, 210),
        (3930, 230)
    ]

    e_params = [
        (500, 80),
        (2000, 156),
        (3130, 190),
        (4150, 220)
    ]

    i_params = [
        (330, 70),
        (2765, 130),
        (3740, 178),
        (4366, 200)
    ]
    o_params = [
        (546, 97),
        (934, 130),
        (2966, 185),
        (3930, 240)
    ]

    u_params = [
        (382, 74),
        (740, 150),
        (2760, 210),
        (3380, 180)
    ]

    plot_H(a_params, Fs, 'A')
    plot_H(e_params, Fs, 'E')
    plot_H(i_params, Fs, 'I')
    plot_H(o_params, Fs, 'O')
    plot_H(u_params, Fs, 'U')
