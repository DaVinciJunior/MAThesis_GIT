import PRAWHelper
import sentHelper
from misc import NonUnicodeEmojis

if __name__ == "__main__":
    PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=10000, func=sentHelper.sent)

    #Bugfixing NonUnicodeEmojis
    # print("?-]")
    # print(NonUnicodeEmojis.demojize("?-]"))

    # print("Hmm da hab ich das gute AZ bekommen. Nice, hätte mir die Tabelle nicht anschauen sollen. :) Was wird für den dritten Stich empfohlen wenn man davor 2x AZ hatte.")
    # print(NonUnicodeEmojis.demojize("Hmm da hab ich das gute AZ bekommen. Nice, hätte mir die Tabelle nicht anschauen sollen. :) Was wird für den dritten Stich empfohlen wenn man davor 2x AZ hatte."))

    ################### FAILED EXPERIMENTS ###################


    # Experiment failed - see function's comment for details
    # PRAWHelper.findAVariantSubmission()