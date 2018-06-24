import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

def poles_zeros_plot(poles, zeros, title):
    ax = plt.subplot(1, 1, 1)
    plt.title(title)
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.grid(linestyle='dashed')
    plt.axis([-2, 2, -2, 2])
    plt.scatter(np.real(poles), np.imag(poles), marker='x', color='red')
    plt.scatter(np.real(zeros), np.imag(zeros), marker='o', color='blue')
    plt.legend(["Polos", "Ceros"])
    plt.axvline(0, color='black')
    plt.axhline(0, color='black')
    ax.add_patch(patches.Circle((0, 0), radius=1, fill=False, ls='dashed', color='black'))

    plt.show()

