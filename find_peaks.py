import numpy as np
import matplotlib as plt
import peakdetect

def peaks_detection(dataset, searching_gap, plot):
    peaks = peakdetect(dataset, lookahead=searching_gap)
    higherPeaks = np.array(peaks[0])
    lowerPeaks = np.array(peaks[1])
    mean_high = np.mean(higherPeaks[:, 1])
    mean_low = np.mean(lowerPeaks[:, 1])

    if plot == True:
        plt.plot(np.arange(0, 6, 0.01), dataset)
        plt.plot(higherPeaks[:, 0] * 0.01, higherPeaks[:, 1], "rx")
        plt.plot(lowerPeaks[:, 0] * 0.01, lowerPeaks[:, 1], "ro")
        plt.xlabel('Time')
        plt.ylabel('Magnitude')
        plt.show()