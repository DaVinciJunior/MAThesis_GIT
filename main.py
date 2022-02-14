import csv
import random

import joblib
from sklearn.model_selection import train_test_split

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

from utils import neuralNetworkUtils
from utils import supportVectorMachineUtils
from utils import prepareTrainingDataUtils
from utils import decisionTreeUtils
from utils import randomForestUtils
from utils import prepareTestDataUtils
from utils import ensembleMethodUtils
from utils import scoreUtils
import glob
import os
from langdetect import detect

def fit_clfs():
    X,Y = prepareTrainingDataUtils.get_same_amount_of_data_for_both_classes()

    nn_clfs = ['nn_1.pkl', 'nn_2.pkl', 'nn_3.pkl']
    svm_clfs = ['svm_1.pkl', 'svm_2.pkl', 'svm_3.pkl']

    for entry in nn_clfs:
        clf = neuralNetworkUtils.load_pickle(entry)
        scoreUtils.show_score(X,Y,clf,'Confusion Matrix ' + entry)

    for entry in svm_clfs:
        clf = supportVectorMachineUtils.load_pickle(entry)
        scoreUtils.show_score(X, Y, clf, 'Confusion Matrix ' + entry)

    n = [5]
    for entry in n:
        ensembleMethodUtils.get_clf(n)
        scoreUtils.show_score(X,Y,clf,'Confusion Matrix Ensemble Method with ' + str(entry) + ' models')
    # plt.show()
    # plt.close('all')
    return clf

if __name__ == "__main__":
#### Test with comment function of bot ####
    # list = ["hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b","hwx761b"]
    # for entry in list:
    #     PRAWHelper.get_comment_by_id_and_reply_de_escalation_to_it(id=entry, placebo=True)
#### Test with comment function of bot ####

#### Test with actual new data from Reddit ####
    clf = ensembleMethodUtils.load_pickle()
    X, Y = prepareTrainingDataUtils.get_same_amount_of_data_for_both_classes()
    frac_test_split = 0.33
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=frac_test_split)
    clf.fit(X_train, y_train)
    scoreUtils.show_score(X_test,y_test,clf,'Confusion Matrix Ensemble Method with 5 models')

    n = 30
    started = datetime.datetime.now()
    print(">>>Starting with the " + str(n) + " newest submissions...<<<\n\n\n")
    PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFeatureFunction(n=n, func=getFeatureSetForText, preprocess=False)
    print("\n\n\n>>>Finished with the " + str(n) + " newest submissions. It needed " + str(datetime.datetime.now() - started) + " time...<<<\n\n\n")

    list_of_files = glob.glob('./logs/*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    # X,additional_data = prepareTestDataUtils.get_n_data_samples(latest_file, 100)
    X,additional_data = prepareTestDataUtils.get_data(latest_file)
    # clf = ensembleMethodUtils.get_clf([5])
    # fit_clfs(clf)
    # clf = fit_clfs()
    pred = clf.predict(X)
    idx = 0

    aggressive_comments = []
    non_aggressive_comments = []

    today = datetime.datetime.now()
    formated_today = today.strftime('%d_%m_%Y_%H_%M')
    dir_path = "./extras/runs/"
    filename = os.path.join(dir_path, formated_today + '.csv')
    file = open(filename, mode="w", encoding="utf-8", newline="")
    writer = csv.writer(file, delimiter =",")
    writer.writerow(["link","text","classification"])

    for idx in range(len(pred)):
        link = additional_data[idx][0]
        text = additional_data[idx][1]
        classification = pred[idx]
        # if comment in other language ignore it
        try:
            if detect(text) == 'de':
                if pred[idx] == 1:
                    aggressive_comments.append([link, text, classification])
                else:
                    non_aggressive_comments.append([link, text, classification])
        except:
            if pred[idx] == 1:
                aggressive_comments.append([link, text, classification])
            else:
                non_aggressive_comments.append([link, text, classification])
        # text = ''
        # for entry in additional_data[idx]:
        #     text = text + '\n' + str(entry).replace('    ', '\n')
        # if pred[idx] == 1:
        #     text = text + '\naggressive'
        #     # Sentiment Analysis was no success unfortunately
        #     # body = sentHelper.preprocessStrings(additional_data[idx][1])
        #     # text = text + '\n\t' + str(sentHelper.sent(body))
        #     aggressive_comments.append(text)
        # else:
        #     text = text + '\nnon-aggressive'
        #     non_aggressive_comments.append(text)

    # Take max #number_of_comments comments of each category and out of context
    number_of_comments = 250
    aggressive_comments = random.sample(aggressive_comments, min(len(aggressive_comments),number_of_comments))
    non_aggressive_comments = random.sample(non_aggressive_comments, min(len(non_aggressive_comments),number_of_comments))

    # print('######################################################################')
    # print('\t\tAggressive Comments')
    for entry in aggressive_comments:
        # print(entry, end='\n---\n')
        writer.writerow(entry)
    # print('######################################################################')
    # print('######################################################################')
    # print('\t\tNon-Aggressive Comments')
    for entry in non_aggressive_comments:
        # print(entry, end='\n---\n')
        writer.writerow(entry)
    print('######################################################################')
    print("Non-aggressive comments: %d\nAggressive comments: %d" % (len(non_aggressive_comments), len(aggressive_comments)))
    file.close()

#### Test with actual new data from Reddit ####

#### Test ensemble method ####
    # X,Y = prepareTrainingDataUtils.get_same_amount_of_data_for_both_classes()
    # frac_test_split = 0.33
    # X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=frac_test_split)
    #
    # # nn_clfs = ['nn_1.pkl', 'nn_2.pkl', 'nn_3.pkl']
    # # svm_clfs = ['svm_1.pkl', 'svm_2.pkl', 'svm_3.pkl']
    #
    # # for entry in nn_clfs:
    # #     clf = neuralNetworkUtils.load_pickle(entry)
    # #     scoreUtils.show_score(X,Y,clf,'Confusion Matrix ' + entry)
    # #
    # # for entry in svm_clfs:
    # #     clf = supportVectorMachineUtils.load_pickle(entry)
    # #     scoreUtils.show_score(X, Y, clf, 'Confusion Matrix ' + entry)
    #
    # clfs = ['_dt_1.pkl', '_dt_2.pkl', '_dt_3.pkl',
    #         '_nn_1.pkl', '_nn_2.pkl', '_nn_3.pkl',
    #         '_rf_1.pkl', '_rf_2.pkl', '_rf_3.pkl',
    #         'rf_max.pkl', 'dt_max.pkl'
    #        ]
    # ensembleMethodUtils.set_clfs(clfs)
    # # clfs_optimal = ['_nn_3.pkl', 'rf_max.pkl', 'dt_max.pkl']
    # # ensembleMethodUtils.set_clfs(clfs_optimal)
    #
    # # n = [3,5,7,9,11]
    # n = [3,5]
    # # n = [3]
    # for entry in n:
    #     ensemble = ensembleMethodUtils.get_clf(n)
    #     ensemble.fit(X_train, y_train)
    #     scoreUtils.show_score(X_test,y_test,ensemble,'Confusion Matrix Ensemble Method with ' + str(entry) + ' models')
    #     joblib.dump(ensemble, './pkl/ensemble_n=' + str(entry) + ' .pkl')
    # plt.show()
#### Test ensemble method ####

#### Train and obtain models ####
    # Dense Neural Network performs pretty well
    # neuralNetworkUtils.generate_pickle()
    # pipeline = neuralNetworkUtils.load_pickle()
    # X_test = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]
    # print('Y_test=' + str(pipeline.predict(X_test)))

    # Support Vector Machines are not practicable
    # supportVectorMachineUtils.generate_pickle()

    # Decision Tree is semi-optimal. Maybe as a third operator in an ensemble method if two better options are delivering different results
    # Optimal results achieved with: depth = 100, r = 101
    # for depth in [10,100,1000,10000,1000000]:
    #     for rando in [101,202,303,404,505]:
    #         print("#################################")
    #         print(str(depth) + ";" + str(rando))
    #         decisionTreeUtils.generate_pickle(depth=depth, random_state=rando)
    #         print("#################################")

    # Random Forest is the best solution.
    # Optimal results achieved for n=100, r=505, l=1
    # for n in [10, 50, 100, 250, 500, 1000]:
    #     for r in [404,505]:
    #         for l in [1, 10, 100]:
    #             print("#################################")
    #             print(n,r,l)
    #             randomForestUtils.generate_pickle(n_estimators = n, random_state=r, min_sample_leaf=l)
    #             print("#################################")

    # Prepare data for ensemble method
    # neuralNetworkUtils.generate_pickle()
    # decisionTreeUtils.generate_pickle(depth=100, random_state=101)
    # randomForestUtils.generate_pickle(n_estimators=100, random_state=505, min_sample_leaf=1)


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