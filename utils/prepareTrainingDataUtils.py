import math
import os
import pandas
import random
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
import prepareTrainingDataUtils

def get_data():
    dir_path = './res/'
    ## File not included in the repository because of concerns regarding data privacy
    filename = os.path.join(dir_path, 'Final Data.csv')
    dataframe = pandas.read_csv(filename, header=None)
    dataset = dataframe.values
    X = dataset[1:, 3:26].astype(float)
    Y = dataset[1:, 26]

    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    return X, encoded_Y


def get_same_amount_of_data_for_both_classes():
    X, encoded_Y = prepareTrainingDataUtils.get_data()
    dict = {
        0: 0,
        1: 0
           }
    ones = []
    zeros = []

    idx = 0
    for entry in encoded_Y:
        dict[entry] = dict[entry] + 1
        if entry == 0:
            zeros.append(idx)
        else:
            ones.append(idx)
        idx = idx + 1

    min = math.inf
    for entry in dict:
        if dict[entry] < min:
            min = dict[entry]

    zeros_indices = random.choices(zeros, k=min)
    ones_indices = random.choices(ones, k=min)

    new_X = []
    new_Y = []
    for entry in zeros_indices:
        new_X.append(X[entry])
        new_Y.append(encoded_Y[entry])
    for entry in ones_indices:
        new_X.append(X[entry])
        new_Y.append(encoded_Y[entry])
    return new_X, new_Y

def normalize_data(X):
    return preprocessing.normalize(X)