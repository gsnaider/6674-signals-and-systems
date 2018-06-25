import matplotlib.pyplot as plt

from util.plot import poles_zeros_plot
from util.speech import vocal_tract_model, A_PARAMS, E_PARAMS, I_PARAMS, O_PARAMS, U_PARAMS

FS = 16000


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
    poles, zeros = plot_H(params, FS, letter)
    poles_zeros_plot(poles, zeros, "Modelo de tracto vocal '%s'\n\nPolos y ceros" % letter)

if __name__ == "__main__":

    exercise(A_PARAMS, 'A')
    exercise(E_PARAMS, 'E')
    exercise(I_PARAMS, 'I')
    exercise(O_PARAMS, 'O')
    exercise(U_PARAMS, 'U')