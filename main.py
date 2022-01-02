import PRAWHelper
import sentHelper
import UnknownWordsLogger
import sys
import datetime
import matplotlib.pyplot as plt

sys.path.insert(1, "./utils/")

from misc import NonUnicodeEmojis
from sentUtils import getCorrectKeyForSentimentAnalysis, getLowerSentimentList, lemmatize
from featureUtils import getFeatureSetForText

import neuralNetworkUtils
import supportVectorMachineUtils
import prepareTrainingDataUtils
import ensembleMethodUtils
import scoreUtils

if __name__ == "__main__":

#### Test ensemble method ####
    X,Y = prepareTrainingDataUtils.get_same_amount_of_data_for_both_classes()

    nn_clfs = ['nn_1.pkl', 'nn_2.pkl', 'nn_3.pkl']
    svm_clfs = ['svm_1.pkl', 'svm_2.pkl', 'svm_3.pkl']

    for entry in nn_clfs:
        clf = neuralNetworkUtils.load_pickle(entry)
        scoreUtils.show_score(X,Y,clf,'Confusion Matrix ' + entry)

    for entry in svm_clfs:
        clf = supportVectorMachineUtils.load_pickle(entry)
        scoreUtils.show_score(X, Y, clf, 'Confusion Matrix ' + entry)

    n = [3,5]
    for entry in n:
        ensembleMethodUtils.get_clf(n)
        scoreUtils.show_score(X,Y,clf,'Confusion Matrix Ensemble Method with ' + str(entry) + ' models')
    plt.show()
    input('Please press \"ENTER\" to proceed (this closes all plots)...')
#### Test ensemble method ####

#### Train and obtain models ####
    # neuralNetworkUtils.generate_pickle()
    # pipeline = neuralNetworkUtils.load_pickle()
    # X_test = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]
    # print('Y_test=' + str(pipeline.predict(X_test)))

    # supportVectorMachineUtils.generate_pickle()
#### Train and obtain models ####

#### Get Data ####
    # n = 1000
    # started = datetime.datetime.now()
    # print(">>>Starting with the " + str(n) + " newest submissions...<<<\n\n\n")
    # PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFeatureFunction(n=n, func=getFeatureSetForText, preprocess=False)
    # print("\n\n\n>>>Finished with the " + str(n) + " newest submissions. It needed " + str(datetime.datetime.now() - started) + " time...<<<\n\n\n")

    # started = datetime.datetime.now()
    # print(">>>Starting with the " + str(n) + " hottest submissions...<<<\n\n\n")
    # PRAWHelper.get_n_LatestSubmissionsInHotAndCommentsAndExecuteFunction(n=n, func=getFeatureSetForText, preprocess=False)
    # print("\n\n\n>>>Finished with the " + str(n) + " hottest submissions. It needed " + str(datetime.datetime.now() - started) + " time...<<<\n\n\n")
#### Get Data ####

#### Get Sentiment ####
    # PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=5, func=sentHelper.sent)
#### Get Sentiment ####

#### "Autotests" ####
    # tests = [
    #     "Impfpflicht ist kein Muss",
    #     "Impfpflich ist ein Muss",
    #     "Ich habe eine Milliarde Euro gewonnen",
    #     "Ich habe eine Milliarde Euro verloren",
    #     "Wir haben eine Milliarde Infizierte in Österreich",
    #     "Wir haben eine Milliarde Geimpfte in Österreich",
    #     "Wen haben wir denn hier?",
    #     "Das Gesundheitspersonal ist überarbeitet",
    #     "Das Gesundheitspersonal ist unterbezahlt",
    #     "Das macht Sinn",
    #     "Das macht doch überhaupt keinen Sinn",
    #     "Das macht keinen Sinn",
    #     "Das macht gar keinen Sinn",
    #     "De Leut hobn an Schodn",
    #     "Die Leut haben einen Schaden",
    #     "Ich brauch einen 3G Nachweis",
    #     "Ich brauche einen 3G Nachweis",
    #     "Die neuen Maßnahmen sind horrende",
    #     "Neue Maßnahmen müssen eingeführt werden",
    #     "Wir werden neue Maßnahmen einführen müssen",
    #     "Das wird uns Milliarden kosten",
    #     "Die Behandlung Ungeimpfter kostet den Staat Milliarden :(",
    #     "😅 ich ich ich :-P ich ich ich 😀",
    #     "Das hier ist ein Satz. Und do red i jetzt gschert.",
    #     "dIe MeDiEn sAn LüGeNpReSsE! /s",
    #     "Hawi!!!",
    #     "Und wenn i di wos frog...???",
    #     "Ich glaube, dass ich die Beistriche richtig anweden kann...",
    #     "Satz 1 hat 5 Wörter. Satz 2 hat 1 Wort mehr!"
    # ]

    # for entry in tests:
    #     features = getFeatureSetForText(entry)
    #     print(entry, features)
        # print(entry, sentHelper.sent(entry))
#### "Autotests" ####

    # UnknownWordsLogger.log()

    ################### FAILED EXPERIMENTS ###################

    # Experiment failed - see function's comment for details
    # PRAWHelper.findAVariantSubmission()