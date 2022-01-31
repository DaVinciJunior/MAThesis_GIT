import joblib
from sklearn.ensemble import VotingClassifier
import neuralNetworkUtils
import supportVectorMachineUtils
import decisionTreeUtils
import randomForestUtils
import scoreUtils
import random

__clfs__ = []

def set_clfs(clfs):
    global __clfs__
    __clfs__ = clfs

def get_clf(n):
    global __clfs__
    tmp_clfs = __clfs__.copy()

    clfs = []
    clfs_names = []

    for i in n:
        clf = None
        file_name = random.choice(tmp_clfs)
        clfs_names.append(file_name[:-4])
        if 'nn' in file_name:
            clf = neuralNetworkUtils.load_pickle(file_name)
        if 'dt' in file_name:
            clf = decisionTreeUtils.load_pickle(file_name)
        if 'rf' in file_name:
            clf = randomForestUtils.load_pickle(file_name)
        tmp_clfs.remove(file_name)
        clfs.append(clf)

    clf = VotingClassifier([(n,c) for n,c in zip(clfs_names,clfs)], voting='hard')
    return clf

# X = Data, n = amount of classifiers that are ensembled (an odd number of values is suggested)
def predict(X, n=3):
    return get_clf(n).predict(X)

def load_pickle():
    return joblib.load('./pkl/ensemble_n=5.pkl')