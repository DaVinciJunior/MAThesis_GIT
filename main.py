import sentHelper
import PRAWHelper

if __name__ == "__main__":
    PRAWHelper.get_n_LatestSubmissionsAndCommentsAndExecuteFunction(n=10000, func=sentHelper.sent)

    ################### FAILED EXPERIMENTS ###################


    # Experiment failed - see function's comment for details
    #PRAWHelper.findAVariantSubmission()