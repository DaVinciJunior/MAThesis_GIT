from textblob_de import TextBlobDE as TextBlob
import re
import emoji
import sys
sys.path.insert(1, "./misc/")
import NonUnicodeEmojis

REGEX_URL_PARSER = r"((\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*)|((mailto:)?[\d\w-]+@[\d\w-]+\.[\d\w-]+)|((www.)[\d\w-]+\.[\d\w-]+))(\/\S+)?"


def preprocessComments(comment):
    # Remove bot replies!
    if comment.author is not None and comment.author.name is not None and comment.body is not None:
        if "bot" in comment.author.name.lower() or "b0t" in comment.author.name.lower():
            comment.author.name = 'BOT'
            comment.body = ''
            return comment
    # Replace unnecessary escaped characters as this otherwise makes problems when analyzing
    comment.body = comment.body.replace("\"", "\\\"")
    comment.body = comment.body.replace("\'", "\\\'")
    # Filter out urls (http, https, ftp, mailto, www., ...)
    comment.body = re.sub(pattern=REGEX_URL_PARSER, repl="", string=comment.body)
    # Replace emojis
    comment.body = emoji.demojize(comment.body)
    # Replace Non-Unicode emojis
    comment = NonUnicodeEmojis.demojize(comment)
    return comment

def sent(text):
    blob = TextBlob(text)
    blob.parse()
    #print(blob.sentences)
    #print(blob.tokens)
    #print(blob.tags)
    #print(blob.noun_phrases)
    #print(text + " - " + str(blob.sentiment) + "\n\n")
    return blob.sentiment