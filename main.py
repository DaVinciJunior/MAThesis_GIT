import PRAWHelper
import sentHelper
import UnknownWordsLogger
from misc import NonUnicodeEmojis

if __name__ == "__main__":
    PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=10000, func=sentHelper.sent)
    UnknownWordsLogger.log()

    ################### FAILED EXPERIMENTS ###################

    # Experiment failed - see function's comment for details
    # PRAWHelper.findAVariantSubmission()