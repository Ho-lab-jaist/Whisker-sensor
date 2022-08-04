import pandas as pd
import csv
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import re
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from peakdetect import peakdetect
from import_data import import_data


def main():
    texture_type = ['Dimplebump', 'Honeycomb', 'Knurklebump']
    list_texture = [['DB_10_10_1', 'DB_10_10_2', 'DB_15_15_1', 'DB_15_15_2', 'DB_20_20_1', 'DB_20_20_2'],
                    ['HC_10_10_1', 'HC_10_10_2', 'HC_15_15_1', 'HC_15_15_2', 'HC_20_20_1', 'HC_20_20_2'],
                    ['KB_10_10_1', 'KB_10_10_2', 'KB_15_15_1', 'KB_15_15_2', 'KB_20_20_1', 'KB_20_20_2']]
    width_length = [[10, 10, 15, 15, 20, 20], [10, 10, 15, 15, 20, 20], [10, 10, 15, 15, 20, 20]]
    height = [[1, 2, 1, 2, 1, 2], [1, 2, 1, 2, 1, 2], [1, 2, 1, 2, 1, 2]]
    ref_feature, ref_processed_data, ref_raw_data = import_data(texture_name=list_texture, texture_class=texture_type,
                                                                width_length=width_length,
                                                                height=height, pressure=100, n_data=50, window_time=600)
    ## spliting data

    x = ref_feature.drop(columns=['A', 'B', 'C', 'Texture_width_length', 'Texture_height'])
    y = ref_feature[['A', 'B', 'C', 'Texture_width_length', 'Texture_height']]
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)


    from sklearn.linear_model import LinearRegression
    from sklearn.multioutput import RegressorChain
    import joblib

    # define model
    LR_model = LinearRegression()
    # fit model
    chainregression = RegressorChain(LR_model, order=[0, 1, 2, 3, 4])
    chain = chainregression.fit(x_train, y_train)
    joblib.dump(chain,
                "C:\\Users\\nhnha\\OneDrive\\Desktop\\Whisker paper\\Frontier 2022\\classifier_py\\LR_clf.joblib")
    print()
    test = chain.predict(x_test)
    LR_score = chainregression.score(x_test, y_test)
    return LR_score
# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()
