import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def plot_fft(signal, title, fs):
    plt.figure(figsize=(6, 2))
    N = len(signal)
    T = 1 / fs
    fft = np.abs(np.fft.fft(signal))
    fft = fft[0 : N // 2]
    freq = np.fft.fftfreq(signal.size, d=T)
    freq = freq[: N // 2]
    plt.plot(freq, fft)
    plt.xlim([0, 6000])
    plt.savefig("out/" + title + ".eps")
    # plt.show() # Uncomment if you want to see the chart
    return fft, freq


def get_integrals(fft, freq, cutoff_freq):
    integral_beforecutoff = 0
    integral_aftercutoff = 0

    for i in range(len(freq)):
        if freq[i] < cutoff_freq:
            integral_beforecutoff += fft[i]
        else:
            integral_aftercutoff += fft[i]
    return integral_beforecutoff, integral_aftercutoff
