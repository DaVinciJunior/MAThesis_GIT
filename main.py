import PRAWHelper
import sentHelper
from misc import NonUnicodeEmojis

if __name__ == "__main__":
    PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=10000, func=sentHelper.sent)

    #Bugfixing NonUnicodeEmojis
    #print("?-]")
    #print(NonUnicodeEmojis.demojize("?-]"))

    ################### FAILED EXPERIMENTS ###################


    # Experiment failed - see function's comment for details
    #PRAWHelper.findAVariantSubmission()