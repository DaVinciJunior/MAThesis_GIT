from sklearn.ensemble import VotingClassifier
import neuralNetworkUtils
import supportVectorMachineUtils
import scoreUtils
import random

def get_clf(n):
    nn_clfs = ['nn_1.pkl', 'nn_2.pkl', 'nn_3.pkl']
    svm_clfs = ['svm_1.pkl', 'svm_2.pkl', 'svm_3.pkl']

    estimators = []

    for i in n:
        clf = None
        if i % 2 == 0:
            file_name = random.choice(nn_clfs)
            clf = neuralNetworkUtils.load_pickle(file_name)
            nn_clfs.remove(file_name)
        else:
            file_name = random.choice(svm_clfs)
            clf = supportVectorMachineUtils.load_pickle(file_name)
            svm_clfs.remove(file_name)
        estimators.append(clf)

    clf = VotingClassifier(estimators)
    return clf

# X = Data, n = amount of classifiers that are ensembled (an odd number of values is suggested)
def predict(X, n=3):
    return get_clf(n).predict(X)