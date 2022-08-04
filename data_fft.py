import pandas as pd
import csv
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import re
import sklearn
def FFT(dataset, plot):
    global dominate_freq
    dt = 1 / 100  # tần số lấy mẫu = 100Hz
    t = np.arange(0, 6, dt)
    n = len(t)
    lowpass_order_filltered = 1
    highpass_order_filltered = 0
    fhat = np.fft.fft(dataset, n)
    mag = np.abs(fhat) / n  # chia cho n =  normalization in the spectral domain
    PSD = fhat * np.conj(fhat) / n
    L = np.arange(1, np.floor(n / 2), dtype='int')
    freq = (1 / (dt * n)) * np.arange(n)
    centroid = np.sum(freq[lowpass_order_filltered:(300 - highpass_order_filltered)]
                      * mag[lowpass_order_filltered:(300 - highpass_order_filltered)]) / np.sum(
        mag[lowpass_order_filltered:(300 - highpass_order_filltered)])
    sum_energy = np.sum(mag[lowpass_order_filltered:(len(L) - highpass_order_filltered)])
    weight_mean_amplitude = np.sum(freq[lowpass_order_filltered:(300 - highpass_order_filltered)]
                                   * mag[lowpass_order_filltered:(300 - highpass_order_filltered)]) / np.sum(
        freq[lowpass_order_filltered:(300 - highpass_order_filltered)])

    max_mag = max(mag[lowpass_order_filltered:-1])
    for i in range(lowpass_order_filltered, len(freq)):
        if abs(mag[i] - max_mag) < 0.00000001:
            dominate_freq = freq[i]
            break
    if plot == True:
        plt.close()
        plt.rcParams['figure.figsize'] = [7, 7]
        plt.rcParams.update({'font.size': 12})
        plt.plot(freq[L], mag[L], color='c', linewidth=2)
        plt.plot([centroid] * len(freq[lowpass_order_filltered:len(L)]), mag[lowpass_order_filltered:len(L)], color='r',
                 linewidth=2)
        #         plt.plot(freq[L],[energy]*len(L))
        plt.text(centroid, 0, 'Spectral centroid = ' + str(centroid), va='top')
        plt.text(25, max_mag / 2, 'Sum energy = ' + str(sum_energy), va='top')
        plt.text(dominate_freq, max_mag, 'dominate frequency = ' + str(dominate_freq), va='top')
        plt.xlim(freq[L[0]], freq[L[-1]])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.show()

    return dominate_freq, freq, mag, max_mag, centroid, sum_energy, fhat
