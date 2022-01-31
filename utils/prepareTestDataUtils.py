import math
import os
import pandas
import random
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
import prepareTrainingDataUtils

def get_data(filename):
    dataframe = pandas.read_csv(filename, header=None)
    dataset = dataframe.values
    additional_data = dataset[1:, :2]
    X = dataset[1:, 2:].astype(float)
    return X, additional_data

def get_n_data_samples(filename, n):
    dataframe = pandas.read_csv(filename, header=None)
    dataset = dataframe.values
    additional_data = dataset[1:, :2]
    X = dataset[1:, 2:].astype(float)

    new_X = []
    new_additional_data = []
    indices = random.sample(range(0,len(X)-1), n)

    for entry in indices:
        new_X.append(X[entry])
        new_additional_data.append(additional_data[entry])

    return new_X, new_additional_data