import PRAWHelper
import sentHelper
import UnknownWordsLogger
from misc import NonUnicodeEmojis

if __name__ == "__main__":
    #PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=10000, func=sentHelper.sent)
    #UnknownWordsLogger.log()

    tests = [
        # "Impfpflicht ist kein Muss",
        # "Impfpflich ist ein Muss",
        # "Ich habe eine Milliarde Euro gewonnen",
        # "Ich habe eine Milliarde Euro verloren",
        # "Wir haben eine Milliarde Infizierte in Österreich",
        # "Wir haben eine Milliarde Geimpfte in Österreich",
        # "Wen haben wir denn hier?",
        # "Das Gesundheitspersonal ist überarbeitet",
        # "Das Gesundheitspersonal ist unterbezahlt",
        # "Das macht Sinn",
        # "Das macht doch überhaupt keinen Sinn",
        # "Das macht keinen Sinn",
        # "Das macht gar keinen Sinn",
        "De Leut hobn an Schodn",
        "Die Leut haben einen Schaden",
        "Ich brauch einen 3G Nachweis",
        "Ich brauche einen 3G Nachweis",
        "Die neuen Maßnahmen sind horrende",
        "Neue Maßnahmen müssen eingeführt werden",
        "Wir werden neue Maßnahmen einführen müssen",
        "Das wird uns Milliarden kosten",
        "Die Behandlung Ungeimpfter kostet den Staat Milliarden"
    ]

    for entry in tests:
        print(entry, sentHelper.sent(entry))

    UnknownWordsLogger.log()

    ################### FAILED EXPERIMENTS ###################

    # Experiment failed - see function's comment for details
    # PRAWHelper.findAVariantSubmission()