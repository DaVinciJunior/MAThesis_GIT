import os
import UnknownWordsLogger

from textblob_de import PatternParserLemmatizer, NLTKPunktTokenizer
from textblob_de.sentiments import Sentiment

MODULE = open("res/textblob-de-location.txt", "r").read()
sentiment = Sentiment(
            path=os.path.join(MODULE, "data", "de-sentiment.xml"),
            synset=None,
            negations=(
                "nicht",
                "ohne",
                "nie",
                "nein",
                "kein",
                "keiner",
                "keine",
                "nichts",
            ),
            modifiers=("RB", "JJ"),
            #modifier=lambda w: w.endswith("lich"),
            #tokenizer = _tokenizer,
            language="de"
        )

_lemmatizer = PatternParserLemmatizer(tokenizer=NLTKPunktTokenizer())

# Get the key without having to care about eventual capitalizings anywhere like in the word GmbH
def getCorrectKeyForSentimentAnalysis(word):
    return [sent for sent in sentiment if word == sent.lower()][0]

def getLowerSentimentList():
    return [sent.lower() for sent in sentiment]

def lemmatize(word):
    return _lemmatizer.lemmatize(word)[0][0].lower()

def checkIfWordIsKnown(word):
    raw = word.lower()
    lemmatized = lemmatize(word).lower()
    if raw in getLowerSentimentList() or lemmatized in getLowerSentimentList():
        return 1
    else:
        UnknownWordsLogger.addWord(raw)
        return 0