from textblob_de import TextBlobDE as TextBlob
import re
import emoji
import sys

import DialectMapper
import UnknownWordsLogger

sys.path.insert(1, "./misc/")
sys.path.insert(2, "./utils/")
from misc import NonUnicodeEmojis
from sentUtils import getCorrectKeyForSentimentAnalysis, getLowerSentimentList, lemmatize
from langdetect import detect

REGEX_URL_PARSER = r"((\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*)|((mailto:)?[\d\w-]+@[\d\w-]+\.[\d\w-]+)|((www.)[\d\w-]+\.[\d\w-]+))(\/\S+)?"
STOP_WORDS = [
    "man", "sich", "vor", "es", "werden", "ein", "die", "das", "dass", "der", "uns", "unser", "und", "noch", "in", "ins", #short form of "in das"
    "weil", "aber", "da", "ja", "sogar", "hier", "auch", "jetzt", "ich", "du", "er", "sie", "es", "wir", "ihr", "ob",
    "mit", "weiter", "denn", "sein", "den", "nur", "bei", "paar", "dem", "am", "vorbei", "zu", "wenn", "dann",
    "von", "an", "auf", "so", "schon", "ist", "sind", "für", "vom", "im", "oder", "wen", "wer", "was", "wessen",
    "weshalb", "warum", "wieso", "welche", "welcher", "welches", "wem", "weswegen", "wie", "wieweit", "wie_weit",
    "wie_viel", "wofür", "wozu", "womit", "wodurch", "worum", "worüber", "wobei", "wovon", "woraus", "wo", "wogegen",
    "wohin", "woher", "woran", "worin", "worauf", "worunter", "wovor", "wohinter", "woneben", "wann", "als", "wird",
    "mir", "mal", "halt", "aus", "mich", "war", "alle", "um", "immer", "nach", "bin", "also", "zum", "dir", "über",
    "wieder", "würden", "würde", "dies", "diese", "mein", "meine", "damit", "eh", "ihm", "ihn", "selbst", "bis", "andere",
    "anderen", "durch", "dazu", "zur", "zum", "eigentlich", "dafür", "gar", "wegen", "seit", "dort", "dein", "deine",
    "unter", "denen", "dich", "gleich", "grunde", "aus", "ab", "etwas", "solange", "schließlich", "schliesslich",
    "bevor", "damals", "davor", "danach"
]

def preprocessComments(comment):
    # Return if body is for some reason empty...
    if comment.body is None:
        return ""
    # Remove bot replies!
    if comment.author is not None and comment.author.name is not None and comment.body is not None:
        if "bot" in comment.author.name.lower() or "b0t" in comment.author.name.lower():
            comment.author.name = 'BOT'
            comment.body = ''
            return comment
    # Remove non-german texts
    try:
        if detect(comment.body) != 'de':
            if comment.author is not None:
                comment.author.name = 'NON-GERMAN-COMMENT'
            comment.body = ''
            return comment
    except:
        do = "nothing"

    # UNNECESSARY!!! Already escaped -> Replace unnecessary escaped characters as this otherwise makes problems when analyzing
    # comment.body = comment.body.replace("\"", "\\\"")
    # comment.body = comment.body.replace("\'", "\\\'")

    # Filter out urls (http, https, ftp, mailto, www., ...)
    comment.body = re.sub(pattern=REGEX_URL_PARSER, repl="", string=comment.body)
    # Replace emojis
    comment.body = emoji.demojize(comment.body)
    # Replace Non-Unicode emojis
    comment = NonUnicodeEmojis.demojize(comment)
    return comment

def preprocessStrings(string):
    # Filter out urls (http, https, ftp, mailto, www., ...)
    string = re.sub(pattern=REGEX_URL_PARSER, repl="", string=string)
    # Replace emojis
    string = emoji.demojize(string)
    # Replace Non-Unicode emojis
    string = NonUnicodeEmojis.demojize(string)
    return string

def sent(text):
    # Replace characters with their appropriate counter-part for analyzing sentiment
    text = re.sub(pattern="“|„|”", repl="\"", string=text)
    text = re.sub(pattern="’|`", repl="\'", string=text)

    text = preprocessStrings(text)
    # Filter out stop words
    filtered_text = ""
    for token in TextBlob(text).words:
        token = token.lower()
        matches_lemmatized = set()
        matches_raw = set()
        all_matches = set()
        raw = token
        lemmatized = lemmatize(token).lower()

        # Only lemmatize if it is actually necessary
        if not (raw in getLowerSentimentList() or lemmatized in getLowerSentimentList()):
            # Dialect mapping
            matches_raw = DialectMapper.mapper(raw)
            matches_lemmatized = DialectMapper.mapper(lemmatized)

            # If one contains matches they might not have been removed for the other. Therefore do this manually!
            if len(matches_raw) > 0:
                UnknownWordsLogger.removeUnknownWordsBecauseOfMatch(lemmatized)
            if len(matches_lemmatized) > 0:
                UnknownWordsLogger.removeUnknownWordsBecauseOfMatch(raw)
        all_matches = matches_raw.union(matches_lemmatized)
        # if some matches found then check all of them before adding them to the filtered text
        if len(all_matches) > 0:
            for subtoken in all_matches:
                if not subtoken in getLowerSentimentList():
                    subtoken = lemmatize(subtoken)
                if not subtoken in STOP_WORDS:
                    filtered_text = filtered_text + " " + subtoken
        # else no matches found or word is by default in the sentiment dictionary
        else:
            # if the lemmatized word in the sentiment list set it first before adding it to the filtered text
            if lemmatized in getLowerSentimentList():
                token = lemmatized
            if not token in STOP_WORDS:
                filtered_text = filtered_text + " " + token
    # print(filtered_text)
    blob = TextBlob(filtered_text)
    blob.parse()
    return blob.sentiment