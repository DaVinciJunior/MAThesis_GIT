import PRAWHelper
import sentHelper
import UnknownWordsLogger
import sys

sys.path.insert(1, "./utils/")

from misc import NonUnicodeEmojis
from sentUtils import getCorrectKeyForSentimentAnalysis, getLowerSentimentList, lemmatize

if __name__ == "__main__":
    PRAWHelper.get_n_LatestSubmissionsInHotAndCommentsAndExecuteFunction(n=1, func=sentHelper.sent)

    # tests = [
    #     # "Impfpflicht ist kein Muss",
    #     # "Impfpflich ist ein Muss",
    #     # "Ich habe eine Milliarde Euro gewonnen",
    #     # "Ich habe eine Milliarde Euro verloren",
    #     # "Wir haben eine Milliarde Infizierte in Österreich",
    #     # "Wir haben eine Milliarde Geimpfte in Österreich",
    #     # "Wen haben wir denn hier?",
    #     # "Das Gesundheitspersonal ist überarbeitet",
    #     # "Das Gesundheitspersonal ist unterbezahlt",
    #     # "Das macht Sinn",
    #     # "Das macht doch überhaupt keinen Sinn",
    #     # "Das macht keinen Sinn",
    #     # "Das macht gar keinen Sinn",
    #     # "De Leut hobn an Schodn",
    #     # "Die Leut haben einen Schaden",
    #     # "Ich brauch einen 3G Nachweis",
    #     # "Ich brauche einen 3G Nachweis",
    #     # "Die neuen Maßnahmen sind horrende",
    #     # "Neue Maßnahmen müssen eingeführt werden",
    #     # "Wir werden neue Maßnahmen einführen müssen",
    #     # "Das wird uns Milliarden kosten",
    #     # "Die Behandlung Ungeimpfter kostet den Staat Milliarden :("
    #     # "ich ich ich :-P ich ich ich"
    # ]
    #
    # for entry in tests:
    #     print(entry, sentHelper.sent(entry))

    UnknownWordsLogger.log()

    ################### FAILED EXPERIMENTS ###################

    # Experiment failed - see function's comment for details
    # PRAWHelper.findAVariantSubmission()