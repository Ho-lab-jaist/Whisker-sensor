import pandas as pd
import csv
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import re
import sklearn
from data_fft import FFT
from data_filter import freq_filter
from find_peaks import peaks_detection

def import_data(texture_class, texture_name, width_length, height, pressure, n_data, window_time):
    index_global = list(range(int(len(texture_class) * len(texture_name[0]) * n_data / 2) * window_time))
    # Time
    time_list = list(range(int(n_data / 2) * window_time))
    total_time = list(range(len(time_list) * len(texture_name[0]) * len(texture_class)))
    for k in range(len(texture_class)):
        for i in range(len(texture_name[0])):
            for j in range(len(time_list)):
                total_time[j + int(n_data / 2) * window_time * i * k] = time_list[j]

    header_raw = [['Time', 'Strain_1_f', 'Strain_2_f'],
                  ['Time', 'Strain_1_b', 'Strain_2_b']]
    header = ['Strain_1_f', 'Strain_2_f', 'Strain_1_b', 'Strain_2_b']
    ## Import raw strain data
    # Main forward data
    strain_data_forward = []
    for texture_folder in range(len(texture_class)):
        os.chdir("Input storage address here"
                 + texture_class[texture_folder] + "\\P = " + str(pressure))
        for filename in texture_name[texture_folder]:
            raw_data_forward = []
            for i in range(int(n_data / 2)):  # number of data for 1 single texture in forward sweeping direction
                raw_csv_forward = pd.read_csv(filename + '_0000_I0' + f"{i * 2:03}" + '.CSV', skiprows=14,
                                              header=None, names=header_raw[0])
                calib_forward_1 = raw_csv_forward['Strain_1_f'][0]
                calib_forward_2 = raw_csv_forward['Strain_2_f'][0]
                for j in range(600):
                    raw_data_forward.append(raw_csv_forward.iloc[250 + j])
                    temp_forward_1 = float(raw_data_forward[600 * i + j]['Strain_1_f']) - calib_forward_1
                    temp_forward_2 = float(raw_data_forward[600 * i + j]['Strain_2_f']) - calib_forward_2
                    raw_data_forward[600 * i + j]['Strain_1_f'] = temp_forward_1
                    raw_data_forward[600 * i + j]['Strain_2_f'] = temp_forward_2
            strain_data_forward.extend(raw_data_forward)
    strain_data_forward = pd.DataFrame(strain_data_forward, index=index_global)
    strain_data_forward = strain_data_forward.drop(columns='Time')
    # Main backward data
    strain_data_backward = []
    for texture_folder in range(len(texture_class)):
        os.chdir("Input storage address here"
                 + texture_class[texture_folder] + "\\P = " + str(pressure))
        for filename in texture_name[texture_folder]:
            raw_data_backward = []
            for i in range(int(n_data / 2)):  # number of data for 1 single texture in forward sweeping direction
                raw_csv_backward = pd.read_csv(filename + '_0000_I0' + f"{i * 2 + 1:03}" + '.CSV', skiprows=14,
                                               header=None, names=header_raw[1])
                calib_backward_1 = raw_csv_backward['Strain_1_b'][0]
                calib_backward_2 = raw_csv_backward['Strain_2_b'][0]
                for j in range(600):
                    raw_data_backward.append(raw_csv_backward.iloc[250 + j])
                    temp_backward_1 = float(raw_data_backward[600 * i + j]['Strain_1_b']) - calib_backward_1
                    temp_backward_2 = float(raw_data_backward[600 * i + j]['Strain_2_b']) - calib_backward_2
                    raw_data_backward[600 * i + j]['Strain_1_b'] = temp_backward_1
                    raw_data_backward[600 * i + j]['Strain_2_b'] = temp_backward_2
            strain_data_backward.extend(raw_data_backward)
    strain_data_backward = pd.DataFrame(strain_data_backward, index=index_global)
    strain_data_backward = strain_data_backward.drop(columns='Time')
    ## Final data frame
    strain_data = (strain_data_forward.join(strain_data_backward)).assign(Time=total_time)


    ## data after noise cancelation
    data = []
    for m in header:
        tempo_data = []
        for i in range(len(texture_class)):
            for j in range(len(texture_name[0])):
                for k in range(int(n_data / 2)):
                    index = range(600 * (int(n_data * len(texture_name[0]) * i / 2) + int(n_data * j / 2) + k),
                                  600 * (int(n_data * len(texture_name[0]) * i / 2) + int(n_data * j / 2) + k + 1))
                    tempo_data.extend((freq_filter(strain_data[m][index], 0.66666667, 20, plot=0))[0])
        data = data + [tempo_data]

    processed_data = []
    for i in range(len(data[0])):
        post_strain_data = []
        for j in range(len(header)):
            post_strain_data.append(data[j][i])
        processed_data.extend([post_strain_data])
    processed_strain_data = (pd.DataFrame(processed_data, columns=header)).assign(Time=total_time)
    ### feature (mean & std) extraction
    feature = []
    tempo_data = []
    for i in range(len(texture_class)):
        for j in range(len(texture_name[0])):
            for k in range(int(n_data / 2)):
                index = range(600 * (int(n_data * len(texture_name[0]) * i / 2) + int(n_data * j / 2) + k),
                              600 * (int(n_data * len(texture_name[0]) * i / 2) + int(n_data * j / 2) + k + 1))
                tempo_data = [np.mean(processed_strain_data['Strain_1_f'][index]),
                              peaks_detection(processed_strain_data['Strain_1_f'][index], 30, 0)[1],
                              FFT(processed_strain_data['Strain_1_f'][index], plot=False)[4],
                              FFT(processed_strain_data['Strain_1_f'][index], plot=False)[0],
                              FFT(processed_strain_data['Strain_1_f'][index], plot=False)[5],
                              np.mean(processed_strain_data['Strain_2_f'][index]),
                              peaks_detection(processed_strain_data['Strain_2_f'][index], 30, 0)[1],
                              FFT(processed_strain_data['Strain_2_f'][index], plot=False)[4],
                              FFT(processed_strain_data['Strain_2_f'][index], plot=False)[0],
                              FFT(processed_strain_data['Strain_2_f'][index], plot=False)[5],
                              np.mean(processed_strain_data['Strain_1_b'][index]),
                              peaks_detection(processed_strain_data['Strain_1_b'][index], 30, 0)[0],
                              FFT(processed_strain_data['Strain_1_b'][index], plot=False)[4],
                              FFT(processed_strain_data['Strain_1_b'][index], plot=False)[0],
                              FFT(processed_strain_data['Strain_1_b'][index], plot=False)[5],
                              np.mean(processed_strain_data['Strain_2_b'][index]),
                              peaks_detection(processed_strain_data['Strain_2_b'][index], 30, 0)[0],
                              FFT(processed_strain_data['Strain_2_b'][index], plot=False)[4],
                              FFT(processed_strain_data['Strain_2_b'][index], plot=False)[0],
                              FFT(processed_strain_data['Strain_2_b'][index], plot=False)[5]]
                feature.append(tempo_data)
    header_feature = ['Mean_Strain_1_f', 'High_peak_1_f', 'Spec_centroid_1_f', 'Dominate_freq_1_f',
                      'Sum_energy_1_f',
                      'Mean_Strain_2_f', 'High_peak_2_f', 'Spec_centroid_2_f', 'Dominate_freq_2_f',
                      'Sum_energy_2_f',
                      'Mean_Strain_1_b', 'High_peak_1_b', 'Spec_centroid_1_b', 'Dominate_freq_1_b',
                      'Sum_energy_1_b',
                      'Mean_Strain_2_b', 'High_peak_2_b', 'Spec_centroid_2_b', 'Dominate_freq_2_b',
                      'Sum_energy_2_b']
    feature = pd.DataFrame(feature, columns=header_feature,
                           index=list(range(len(texture_class) * len(texture_name[0]) * int(n_data / 2))))

    ## Final dataframe
    a = []
    b = []
    c = []
    texture_width_length = []
    texture_height = []
    texture_type = ['Dimplebump', 'Dimplebump_cut1', 'Dimplebump_cut5', 'Honeycomb', 'Honeycomb_cut1'
        , 'Honeycomb_cut5', 'Knurklebump', 'Knurklebump_cut1', 'Knurklebump_cut5']
    for i in range(len(texture_class)):
        for j in range(len(texture_name[0])):
            for k in range(int(n_data / 2)):
                if texture_class[i] == texture_type[0]:
                    a.append(1)
                    b.append(0)
                    c.append(0)
                elif texture_class[i] == texture_type[1]:
                    a.append(1)
                    b.append(0)
                    c.append(0)
                elif texture_class[i] == texture_type[2]:
                    a.append(1)
                    b.append(0)
                    c.append(0)
                elif texture_class[i] == texture_type[3]:
                    a.append(0)
                    b.append(1)
                    c.append(0)
                elif texture_class[i] == texture_type[4]:
                    a.append(0)
                    b.append(1)
                    c.append(0)
                elif texture_class[i] == texture_type[5]:
                    a.append(0)
                    b.append(1)
                    c.append(0)
                else:
                    a.append(0)
                    b.append(0)
                    c.append(1)
                texture_width_length.append(width_length[i][j])
                texture_height.append(height[i][j])

    feature = feature.assign(A=a, B=b, C=c, Texture_width_length=texture_width_length, Texture_height=texture_height)

    return feature, processed_strain_data, strain_data