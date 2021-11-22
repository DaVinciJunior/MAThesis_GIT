import os
import re
import UnknownWordsLogger
import itertools
import sys

sys.path.insert(1, "./utils/")
from textblob_de.sentiments import Sentiment
from sentUtils import getCorrectKeyForSentimentAnalysis, getLowerSentimentList, lemmatize

MODULE = "C:\\Users\\tugbil\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\textblob_de\\"

previous_mappings = {}

# Pattern followed by what it should be replaced with
replacements = [
    ["", ""],           # empty set to leave one empty for recursions
    ### A ###
    ["a$", "ei"],       # e.g. "zwa" -> "zwei", "Gib ma zwa bia" -> "Gib mir zwei Bier"
    ["a$", "ein"],      # e.g. "a" -> "ein", "Gib ma a bia" -> "Gib mir ein Bier"
    ["a$", "er"],       # e.g. "via" -> "vier", "Ka bia voa via" -> "Kein Bier vor vier"
    ["a$", "r"],        # e.g. "voa" -> "vor", "Ka bia voa via" -> "Kein Bier vor vier"
    ["^a", ""],         # e.g. "amol" -> "mal", "Hold des amol" -> "Halte das mal"
    ["ae", "ä"],
    ["a", "ä"],         # e.g. "leberkas" -> "leberkäs"
    ["^aufg", "aufge"], # e.g. "aufgmacht" -> "aufgemacht"
    ### B ###
    ["b$", "be"],       # e.g. "hob" -> "habe"
    ### C ###
    ### D ###
    ["d$", "te"],       # e.g. "hold" -> "halte", "Hold des amol" -> "Halte das mal"
    ["d$", "t"],        # e.g. "hold" -> "halt"
    ["d$", "den"],      # e.d. "meld" -> "melden"
    ### E ###
    ["e$", "ie"],       # e.g. "de" -> "die", "De koaten hob i scho" -> "Die Karte habe ich schon"
    ["e", "ee"],        # e.g. "shesh" -> "sheesh"
    ["ee", "e"],        # e.g. "sheeeesh" -> "sheesh"
    ["e", "i"],         # e.g. "werd" -> "wird"
    ["e", "ö"],         # e.g. "bled" -> "blöd", "A blede Gschicht" -> "Eine blöde Geschichte"
    ["e$", "en"],       # e.g. "brauche" -> "brauchen", should technically be fixed by lemmatizer but it isn't unfortunately
    ### F ###
    ### G ###
    ["^g", "ge"],       # e.g. "gongen" -> "gegangen"
    ["^g", ""],
    ["go", "geg"],      # e.g. "gongen" -> "gegangen"
    ["g$", "ge"],       # e.g. "solang" -> "solange"
    ### H ###
    ["h$", "he"],       # e.g. "brauch" -> "brauche"
    ["h$", "ht"],       # e.g. "nit" -> "nicht"
    ### I ###
    ["ia$", "ür"],      # e.g. "tia" -> "tür"
    ["ia", "ihr"],      # e.g. "ia" -> "ihr", "Ia seids jo irr" -> "Ihr seid ja irre"
    ["i", "u"],         # e.g. "neies" -> "neues"
    ["i", "ich"],       # e.g. "nit" -> "nicht"
    ### J ###
    ### K ###
    ### L ###
    ["l", "ll"],        # e.g. "alan" -> "allein"
    ### M ###
    ### N ###
    ["n$", "en"],       # e.g. "reissn" -> "reissen"
    ["n$", "ne"],       # e.g. "scheun" -> "scheune"
    ["^na$", "nein"],
    ["^nimmer$", "nicht"], # technically "nicht mehr" but it is sufficient as it is
    ["^ne$", "ein"],
    ### O ###
    ["o", "a"],         # e.g. "hob" -> "habe"
    ["o", "i"],         # e.g. "hoid" -> "halte", "Hoid des amol" -> "Halte das mal"
    ["o", "oo"],        # e.g. "of" -> "oof"
    ["o", "och"],       # e.g. "no" -> "noch"
    ["oo", "o"],        # e.g. "ooof" -> "oof"
    ["oa", "ar"],       # e.g. "koatn" -> "Karte", "De koaten hob i scho" -> "Die Karte habe ich schon"
    ["oe", "ö"],
    ### P ###
    ### Q ###
    ### R ###
    ["rl$", ""],        # e.g. "zungenspitzerl" -> "zungenspitze"
    ### S ###
    ["s$", "se"],       # e.g. "scheiß" -> "scheiße"
    ["s$", "st"],       # e.g. "is" -> "ist"
    ["s$", "ss"],       # e.g. "muas" -> "muss"
    ["ss", "ß"],
    ["ß", "ss"],
    ["^schmäh$", "scherz"],
    ### T ###
    ["t$", "te"],       # e.g. "hoit" -> "halte", "Hoit des amol" -> "Halte das mal"
    ["t$", "n"],        # e.g. "kostet" -> "kosten", should technically be fixed by lemmatizer but it isn't unfortunately
    ["ts$", "t"],       # e.g. "gibts" -> "gibt"
    ### U ###
    ["u", "o"],         # e.g. "sunsd" -> "sonst"
    ["ua", "u"],        # e.g. "muass" -> "muss"
    ["ue", "ü"],
    ["ui$", "oll"],     # e.g. "vui" -> "voll", "Da film gfoit ma vui" -> "Der Film gefällt mir voll"
    ["ü$", "iel"],      # e.g. "vü" -> "viel, "Es kost halt so vü" -> "Es kostet halt so viel"
    ### V ###
    ### W ###
    ### X ###
    ["x$", "cht"],      # e.g. "nix" -> "nicht(s)", "Bei mir gibts nix neies" -> "Bei mir gibt es nichts neues"
    ["x", "er"],        # e.g. "wixer" -> "wichser"
    ### Y ###
    ### Z ###
    ["tz$", "tzt"],     # e.g. "jezt" -> "jetzt"
    ["zt$", "tzt"]      # e.g. "jezt" -> "jetzt"
]

def mapper(word):
    if word in getLowerSentimentList():
        word = getCorrectKeyForSentimentAnalysis(word)
        return word
    elif word in previous_mappings.keys():
        return previous_mappings[word]
    else:
        UnknownWordsLogger.addWord(word)
        # Start mapping procedure
        matches = replacing(word)
        # if a word occurs multiple times reuse the mapping
        previous_mappings[word] = matches
        # all matches get returned as we cannot guarantee which of the matches is the correct one. The sentiment will anyhow be averaged
        return matches

def replacing(word):
    matches = set()
    # for rep1, rep2, rep3 in itertools.combinations(replacements, 3):
    for rep1, rep2 in itertools.combinations(replacements, 2):
        new_word = word
        # reps = [rep1, rep2, rep3]
        reps = [rep1, rep2]
        for rep in reps:
            new_word = re.sub(pattern=rep[0], repl=rep[1], string=new_word)
            matches = handle_potential_new_word(matches, new_word, word)
    # print(word, "->", matches)
    return matches


def handle_potential_new_word(matches, new_word, word):
    if new_word in getLowerSentimentList():
        new_word = getCorrectKeyForSentimentAnalysis(new_word)
        matches.add(new_word)
        UnknownWordsLogger.addPossibleMapping(word, new_word)
    try:
        if lemmatize(new_word) in getLowerSentimentList():
            new_word = getCorrectKeyForSentimentAnalysis(lemmatize(new_word))
            matches.add(new_word)
            UnknownWordsLogger.addPossibleMapping(word, new_word)
    except:
        do = "nothing"
    return matches