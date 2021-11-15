from textblob_de import TextBlobDE as TextBlob
import re
import emoji
import sys
sys.path.insert(1, "./misc/")
from misc import NonUnicodeEmojis

REGEX_URL_PARSER = r"((\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*)|((mailto:)?[\d\w-]+@[\d\w-]+\.[\d\w-]+)|((www.)[\d\w-]+\.[\d\w-]+))(\/\S+)?"
STOP_WORDS = [
    "man",
    "sich",
    "vor",
    "es",
    "werden",
    "ein",
    "die",
    "das",
    "der",
    "uns",
    "unser",
    "und",
    "noch",
    "in",
    "ins", #short form of "in das"
    "weil",
    "aber",
    "da",
    "ja",
    "sogar",
    "hier",
    "auch",
    "jetzt",
    "ich",
    "ob",
    "mit",
    "weiter",
    "denn",
    "doch"
]


def preprocessComments(comment):
    # Remove bot replies!
    if comment.author is not None and comment.author.name is not None and comment.body is not None:
        if "bot" in comment.author.name.lower() or "b0t" in comment.author.name.lower():
            comment.author.name = 'BOT'
            comment.body = ''
            return comment

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

def sent(text):
    # Replace characters with their appropriate counter-part for analyzing sentiment
    text = re.sub(pattern="“|„|”", repl="\"", string=text)
    text = re.sub(pattern="’|`", repl="\'", string=text)

    # TODO: Add Dialect mapping

    # Filter out stop words
    filtered_text = ""
    for token in TextBlob(text).tokenize():
        if not TextBlob(token.lower()).parse() in STOP_WORDS:
            filtered_text = filtered_text + " " + token

    blob = TextBlob(filtered_text)
    blob.parse()
    return blob.sentiment