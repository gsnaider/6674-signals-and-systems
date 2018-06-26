import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav

from util.speech import glottal_pulse, A_PARAMS, E_PARAMS, I_PARAMS, O_PARAMS, U_PARAMS, sintetize

FILTER_COEFS = [
    0.007290901623811003,
    0.006998116892010644,
    0.006588240635016143,
    0.006059422368458391,
    0.005410925594604318,
    0.004643158445822491,
    0.003757692698348427,
    0.002757270812382158,
    0.001645800784677901,
    0.000428338733327909,
    -0.000888940730120864,
    -0.002298786150300013,
    -0.003792922573926957,
    -0.005362116134729513,
    -0.006996249292658398,
    -0.008684406020982915,
    -0.010414966120413665,
    -0.012175707733517898,
    -0.013953917036642253,
    -0.015736504001479624,
    -0.017510123045333045,
    -0.019261297328925300,
    -0.020976545414017712,
    -0.022642508960718358,
    -0.024246080126598124,
    -0.025774527326844782,
    -0.027215618026749377,
    -0.028557737264742328,
    -0.029790000645712477,
    -0.030902360600014594,
    -0.031885704772799506,
    -0.032731945490325966,
    -0.033434099343827656,
    -0.033986356036263786,
    -0.034384135751704341,
    -0.034624134429903641,
    0.965295643541587478,
    -0.034624134429903641,
    -0.034384135751704341,
    -0.033986356036263786,
    -0.033434099343827656,
    -0.032731945490325966,
    -0.031885704772799506,
    -0.030902360600014594,
    -0.029790000645712477,
    -0.028557737264742328,
    -0.027215618026749377,
    -0.025774527326844782,
    -0.024246080126598124,
    -0.022642508960718358,
    -0.020976545414017712,
    -0.019261297328925300,
    -0.017510123045333045,
    -0.015736504001479624,
    -0.013953917036642253,
    -0.012175707733517898,
    -0.010414966120413665,
    -0.008684406020982915,
    -0.006996249292658398,
    -0.005362116134729513,
    -0.003792922573926957,
    -0.002298786150300013,
    -0.000888940730120864,
    0.000428338733327909,
    0.001645800784677901,
    0.002757270812382158,
    0.003757692698348427,
    0.004643158445822491,
    0.005410925594604318,
    0.006059422368458391,
    0.006588240635016143,
    0.006998116892010644,
    0.007290901623811003,
]

def spectral_analysis(sintetized, filtered, fs, f0, letter):
    X = np.fft.fft(sintetized) / len(sintetized)
    X_fil = np.fft.fft(filtered) / len(filtered)

    freqs = np.arange(0, fs, fs / len(X))

    plt.figure()
    plt.title("Espectro de amplitud de '%s' filtrada" % letter)
    plt.plot(freqs, np.absolute(X))
    plt.plot(freqs, np.absolute(X_fil))

    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("|X(ω)|")
    plt.legend(["Señal original", "Señal filtrada"])

    plt.show()

def exercise(glottal_pulse, fs, f0, vowel_params, letter):
    sintetized = sintetize(glottal_pulse, fs, vowel_params)
    filtered = np.convolve(sintetized, FILTER_COEFS)

    x_start = len(filtered) - len(sintetized)
    filtered = filtered[x_start:]

    wav.write("../data/%s_filt.wav" % letter, fs, filtered)

    plt.figure()
    plt.title("Señales de audio de '%s'" % letter)
    plt.plot(sintetized[:500])
    plt.plot(filtered[:500])
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.legend(["Señal original", "Señal filtrada"])
    plt.grid(linestyle="dashed")
    plt.show()

    spectral_analysis(sintetized, filtered, fs, f0, letter)



if __name__ == "__main__":
    fs = 16000
    f0 = 200
    glot, _ = glottal_pulse(f0, Tp_pct=0.4, Tn_pct=0.16, P0=1, periods=200, fs=fs)

    # exercise(glot, fs, f0, A_PARAMS, 'A')
    exercise(glot, fs, f0, E_PARAMS, 'E')
    exercise(glot, fs, f0, I_PARAMS, 'I')
    exercise(glot, fs, f0, O_PARAMS, 'O')
    exercise(glot, fs, f0, U_PARAMS, 'U')