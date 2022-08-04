import pandas as pd
import csv
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import re
import sklearn
from data_fft import FFT
def freq_filter(dataset, low_cut_freq, high_cut_freq, plot):
    dt = 1 / 100  # tần số lấy mẫu = 100Hz
    t = np.arange(0, 6, dt)
    n = len(t)
    dominate_freq, freq, mag, max_mag, centroid, energy, fhat = FFT(dataset, plot=False)
    indices = np.logical_or(np.logical_and(freq > low_cut_freq, freq < high_cut_freq),
                            np.logical_and(freq > 100 - high_cut_freq, freq < 100 - low_cut_freq))
    indices[0] = True
    L = np.arange(1, np.floor(n / 2), dtype='int')
    clean_mag = mag * indices
    fhat = indices * fhat

    ffilt = (np.fft.ifft(fhat)).real
    if plot == True:
        fig, axs = plt.subplots(2, 1, sharex=False, sharey=False)
        plt.sca(axs[0])
        plt.plot(t, ffilt, linewidth=2, color='c', label='Filtered')
        plt.plot(np.arange(0, 6, dt), dataset, color='r', linewidth=2, label='Raw')
        plt.legend()
        plt.xlabel('Time (s)')
        plt.ylabel('Magnitude')

        plt.sca(axs[1])
        plt.plot(freq[L], clean_mag[L], color='c', linewidth=2, label='Filtered')
        plt.plot(freq[L], mag[L], color='r', linewidth=2, label='Raw')
        plt.xlim(freq[L[0]], freq[L[-1]])
        plt.legend()
        plt.xlabel('Frequency')
        plt.ylabel('Magnitude')

        fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.title('Comparison data in time domain after filtering')
    return ffilt, clean_mag