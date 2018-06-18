from scipy.io import wavfile as wav

from util.input import A_PERIOD_START, A_PERIOD_END, letters, O_PERIOD_END, O_PERIOD_START, I_PERIOD_START, I_PERIOD_END
from util.signal import sub_signal, plot_specgram

def exercise(x, fs, letter, T):
    x_letter, _ = sub_signal(x, fs, letter.start, letter.end)
    periods = 10
    length_window = int(T * fs * periods)
    plot_specgram(x_letter, fs, length_window, letter.char)

if __name__ == "__main__":
    (fs, x) = wav.read("../data/hh15.WAV")

    letter_a = letters[7]
    T_a = A_PERIOD_END - A_PERIOD_START
    exercise(x, fs, letter_a, T_a)

    letter_o = letters[1]
    T_o = O_PERIOD_END - O_PERIOD_START
    exercise(x, fs, letter_o, T_o)

    letter_i = letters[13]
    T_i = I_PERIOD_END - I_PERIOD_START
    exercise(x, fs, letter_i, T_i)