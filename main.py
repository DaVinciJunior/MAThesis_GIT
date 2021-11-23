import PRAWHelper
import sentHelper
import UnknownWordsLogger
import sys
import datetime

sys.path.insert(1, "./utils/")

from misc import NonUnicodeEmojis
from sentUtils import getCorrectKeyForSentimentAnalysis, getLowerSentimentList, lemmatize
from featureUtils import getFeatureSetForText

if __name__ == "__main__":
    n = 1000
    started = datetime.datetime.now()
    print(">>>Starting with the " + str(n) + " newest submissions...<<<\n\n\n")
    PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFeatureFunction(n=n, func=getFeatureSetForText, preprocess=False)
    print("\n\n\n>>>Finished with the " + str(n) + " newest submissions. It needed " + str(datetime.datetime.now() - started) + " time...<<<\n\n\n")

    # started = datetime.datetime.now()
    # print(">>>Starting with the " + str(n) + " hottest submissions...<<<\n\n\n")
    # PRAWHelper.get_n_LatestSubmissionsInHotAndCommentsAndExecuteFunction(n=n, func=getFeatureSetForText, preprocess=False)
    # print("\n\n\n>>>Finished with the " + str(n) + " hottest submissions. It needed " + str(datetime.datetime.now() - started) + " time...<<<\n\n\n")

    # PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=5, func=sentHelper.sent)

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

    UnknownWordsLogger.log()

    ################### FAILED EXPERIMENTS ###################

    # Experiment failed - see function's comment for details
    # PRAWHelper.findAVariantSubmission()