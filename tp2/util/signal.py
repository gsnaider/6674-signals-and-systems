import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks_cwt

def sub_signal(x, fs, start, end):
    sub_x = x[int(start * fs): int(end * fs)]
    sub_t = np.arange(0, len(sub_x) / fs, 1 / fs) + start
    return sub_x, sub_t


def plot_fourier_coefficients(X, plot_title):
    plt.figure()
    plt.suptitle(plot_title, fontsize=16)

    plt.subplot(2, 1, 1)
    plt.title("Módulo")
    plt.xlabel('k')
    plt.ylabel('|ak|')
    plt.grid(linestyle='dashed')
    plt.stem(np.absolute(X))

    plt.subplot(2, 1, 2)
    plt.title("Fase")
    plt.xlabel('k')
    plt.ylabel('< ak')
    plt.grid(linestyle='dashed')
    plt.stem(np.angle(X))

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def plot_period(x, t, name):
    start = x[0]
    end = x[len(x) - 1]
    print('Period start value:\t', start)
    print('Period end value:\t', end)
    print('Difference:\t', abs(end - start))

    plt.figure()
    plt.grid(linestyle='dashed')
    plt.title("Periodo de '%s'" % name)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Señal')
    plt.plot(t, x)
    plt.show(block=False)


def plot_specgram(x, fs, length_window, name):
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.suptitle('Señal y Espectrograma de %s' % name, fontsize=16)

    t = np.arange(0, len(x) / fs, 1 / fs)
    plt.grid(linestyle='dashed')
    plt.plot(t, x)
    plt.title("Señal")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Señal")

    plt.subplot(2, 1, 2)
    plt.specgram(x, NFFT=length_window, Fs=fs, noverlap=length_window // 2)
    plt.title("Espectrograma")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Frecencia [Hz]")

    plt.subplots_adjust(hspace=0.5)
    plt.show()

def cepstrum(x):
    return np.fft.ifft(np.log(np.abs(np.fft.fft(x))))


def PSOLA(x, fs, sonorous_segments, f0s, new_f0_pct, plot=True):

    for sonorous_segment in sonorous_segments:
        x_start = int(sonorous_segment[0] * fs)
        x_end = int(sonorous_segment[1] * fs)
        x_segment = x[x_start:x_end]
        peaks_idxs = find_peaks_cwt(x_segment, np.arange(1, 100))

        diffs = []
        prev = None
        for peak in peaks_idxs:
            if (prev != None):
                diffs.append(peak - prev)
            prev = peak
        mean_diff = np.mean(np.array(diffs))

        # Tomamos aproximadamente 2 periodos como ancho de ventana
        window_size = int(mean_diff * 2)

        windows = []
        for peak_idx in peaks_idxs[1:-1]:
            window = np.hanning(window_size)
            win_start = peak_idx - window_size // 2
            win_end = win_start + len(window)

            # if(win_start < 0):
            #     window = window[-win_start:]
            #     win_start = 0
            # if (win_end > len(x_segment)):
            #     window = window[:]

            full_window = np.zeros(len(x_segment))
            full_window[win_start:win_end] = window
            windows.append(full_window)

        start_idx = np.nonzero(windows[0])[0][0]
        end_idx = np.nonzero(windows[-1])[0][-1]
        starting_x_window = np.zeros(len(x_segment))
        starting_x_window[:start_idx] = 1
        starting_x_window[end_idx:] = 1

        segmented_x = x_segment * starting_x_window
        for window in windows:
            segmented_x += x_segment * window

        if (plot):
            t = np.arange(0, len(x) / fs, 1 / fs)[x_start:x_end]
            plt.figure()
            plt.plot(t, x_segment)
            for peak_idx in peaks_idxs:
                plt.axvline(x=t[peak_idx], color='r', linestyle='dotted')

                # win_start = peak_idx - window_size // 2
                # win_end = min(win_start + len(window), len(t))
                #
                # if (win_start < 0):
                #     plt.plot(t[win_start:win_end], window[:win_end - win_start] * max(x_segment))
                # else:
                #     plt.plot(t[win_start:win_end], window[:win_end-win_start]*max(x_segment))

                plt.show()

            for wind in windows:
                plt.plot(t, wind*max(x_segment), color='orange')
            plt.show()

            plt.figure()
            plt.plot(t, x_segment)
            plt.plot(t, segmented_x)
            plt.show()
            plot = False # Only plot first