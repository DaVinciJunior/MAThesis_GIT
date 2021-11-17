import os
import re
import UnknownWordsLogger
import itertools
import sys

sys.path.insert(1, "./utils/")
from textblob_de.sentiments import Sentiment
from sentUtils import getCorrectKeyForSentimentAnalysis, getLowerSentimentList, lemmatize

MODULE = "C:\\Users\\tugbil\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\textblob_de\\"

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

# Pattern followed by what it should be replaced with
replacements = [
    ["", ""],       # empty set to leave one empty for recursions
    ### A ###
    ["a$", "ei"],    # e.g. "zwa" -> "zwei", "Gib ma zwa bia" -> "Gib mir zwei Bier"
    ["a$", "ein"],   # e.g. "a" -> "ein", "Gib ma a bia" -> "Gib mir ein Bier"
    ["a$", "er"],    # e.g. "via" -> "vier", "Ka bia voa via" -> "Kein Bier vor vier"
    ["a$", "r"],     # e.g. "voa" -> "vor", "Ka bia voa via" -> "Kein Bier vor vier"
    ["^a", ""],      # e.g. "amol" -> "mal", "Hold des amol" -> "Halte das mal"
    ### B ###
    ["b$", "be"],    # e.g. "hob" -> "habe"
    ### C ###
    ### D ###
    ["d$", "te"],    # e.g. "hold" -> "halte", "Hold des amol" -> "Halte das mal"
    ["d$", "t"],     # e.g. "hold" -> "halt"
    ### E ###
    ["e$", "ie"],    # e.g. "de" -> "die", "De koaten hob i scho" -> "Die Karte habe ich schon"
    ["e", "i"],     # e.g. "werd" -> "wird"
    ["e", "ö"],     # e.g. "bled" -> "blöd", "A blede Gschicht" -> "Eine blöde Geschichte"
    ["e$", "en"],    # e.g. "brauche" -> "brauchen", should technically be fixed by lemmatizer but it isn't unfortunately
    ### F ###
    ### G ###
    ["^g", "ge"],    # e.g. "gongen" -> "gegangen"
    ### H ###
    ["h$", "he"],    # e.g. "brauch" -> "brauche"
    ### I ###
    ["ia$", "ür"],   # e.g. "tia" -> "tür"
    ["ia", "ihr"],   # e.g. "ia" -> "ihr", "Ia seids jo irr" -> "Ihr seid ja irre"
    ### J ###
    ### K ###
    ### L ###
    ["l", "ll"],    # e.g. "alan" -> "allein"
    ### M ###
    ### N ###
    ["n$", "en"],    # e.g. "reissn" -> "reissen"
    ["n$", "ne"],    # e.g. "scheun" -> "scheune"
    ### O ###
    ["o", "a"],     # e.g. "hob" -> "habe"
    ["o", "i"],     # e.g. "hoid" -> "halte", "Hoid des amol" -> "Halte das mal"
    ["oa", "ar"],   # e.g. "koatn" -> "Karte", "De koaten hob i scho" -> "Die Karte habe ich schon"
    ["oa", "ohr"],  # e.g. "oawaschl" -> "Ohr"
    ### P ###
    ### Q ###
    ### R ###
    ### S ###
    ### T ###
    ["t$", "te"],     # e.g. "hoit" -> "halte", "Hoit des amol" -> "Halte das mal"
    ["t$", "n"],      # e.g. "kostet" -> "kosten", should technically be fixed by lemmatizer but it isn't unfortunately
    ### U ###
    ["ui$", "oll"],   # e.g. "vui" -> "voll", "Da film gfoit ma vui" -> "Der Film gefällt mir voll"
    ["ü$", "iel"],    # e.g. "vü" -> "viel, "Es kost halt so vü" -> "Es kostet halt so viel"
    ### V ###
    ### W ###
    ### X ###
    ### Y ###
    ### Z ###
]

def mapper(word):
    if word in getLowerSentimentList():
        word = getCorrectKeyForSentimentAnalysis(word)
        return word
    else:
        UnknownWordsLogger.addWord(word)
        # Start mapping procedure
        matches = replacing(word)
        # all matches get returned as we cannot guarantee which of the matches is the correct one. The sentiment will anyhow be averaged
        return matches

def replacing(word):
    matches = set()
    for rep1, rep2, rep3 in itertools.combinations(replacements, 3):
        new_word = word
        reps = [rep1, rep2, rep3]
        for rep in reps:
            new_word = re.sub(pattern=rep[0], repl=rep[1], string=new_word)
            matches = handle_potential_new_word(matches, new_word, word)
    return matches


def handle_potential_new_word(matches, new_word, word):
    if new_word in getLowerSentimentList():
        new_word = getCorrectKeyForSentimentAnalysis(new_word)
        matches.add(new_word)
        UnknownWordsLogger.addPossibleMapping(word, new_word)
    if lemmatize(new_word) in getLowerSentimentList():
        new_word = getCorrectKeyForSentimentAnalysis(lemmatize(new_word))
        matches.add(new_word)
        UnknownWordsLogger.addPossibleMapping(word, new_word)
    return matches