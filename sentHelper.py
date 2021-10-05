from textblob_de import TextBlobDE as TextBlob

def sent(text):
    blob = TextBlob(text)
    blob.parse()
    print(blob.sentences)
    print(blob.tokens)
    print(blob.tags)
    print(blob.noun_phrases)
    print(text + " - " + str(blob.sentiment) + "\n\n")