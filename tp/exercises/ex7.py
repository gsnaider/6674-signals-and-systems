import matplotlib.pyplot as plt

from util.plot import poles_zeros_plot
from util.speech import vocal_tract_model

FS = 16000

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


def plot_H(params, Fs, letter):
    H, w, Hs, poles, zeros = vocal_tract_model(params, Fs)
    plt.figure()
    for Hn in Hs:
        plt.plot(w, abs(Hn), dashes=[6, 2])
    plt.plot(w, abs(H))
    plt.grid(linestyle='dashed')
    plt.title("Modelo de tracto vocal '%s'\n\nRespuesta en frecuencia" % letter)

    # TODO checkear como pasar de ω a Hz
    plt.xlabel("ω")

    plt.ylabel("|H(ω)|")
    plt.legend(["H1", "H2", "H3", "H4", "H"])
    plt.show()
    plt.figure()

    return (poles, zeros)


def exercise(params, letter):
    poles, zeros = plot_H(A_PARAMS, FS, letter)
    poles_zeros_plot(poles, zeros, "Modelo de tracto vocal '%s'\n\nPolos y ceros" % letter)

if __name__ == "__main__":

    exercise(A_PARAMS, 'A')
    exercise(E_PARAMS, 'E')
    exercise(I_PARAMS, 'I')
    exercise(O_PARAMS, 'O')
    exercise(U_PARAMS, 'U')