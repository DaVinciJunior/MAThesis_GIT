import re
import math
import os
import csv

from textblob_de import TextBlobDE as TextBlob
from sentUtils import checkIfWordIsKnown
from sentHelper import preprocessStrings
from datetime import datetime

file = open("./res/dialectalRegExs.txt", encoding="utf-8")
# get dialectal regexes from list
dialectal_regexes = file.read().split(",")

file = open("./res/triggerWordsRegExs.txt", encoding="utf-8")
# get trigger words from list
trigger_regexes = file.read().split(",")

today = datetime.now()
formated_today = today.strftime('%d_%m_%Y_%H_%M')

dir_path = "./logs/"
filename = os.path.join(dir_path, formated_today + '.csv')
file = open(filename, mode="w", encoding="utf-8", newline="")
writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
writer.writerow(["link","text","number_of_words_that_start_with_a_capital_letter","number_of_capital_letters",
                 "number_of_words","number_of_unknown_words","number_of_words_that_contain_dialectal_words",
                 "average_word_length","max_word_length","min_word_length","average_number_of_words_per_sentence",
                 "max_number_of_words_per_sentence","min_number_of_words_per_sentence","number_of_emojis",
                 "average_number_of_emojis_per_sentence","number_of_urls","number_of_question_marks",
                 "number_of_call_signs","number_of_dots","number_of_commas","number_of_digits",
                 "number_of_sarcasm_indicators","number_of_trigger_words","upvotes","replies"])

emoji_regex = ":(\S)+:"
url_regex = r"((\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*)|((mailto:)?[\d\w-]+@[\d\w-]+\.[\d\w-]+)|((www.)[\d\w-]+\.[\d\w-]+))(\/\S+)?"

def getFeatureSetForText(text, upvotes=0, replies=0, submissionId=None, commentId=None):
    writer = csv.writer(file)
    number_of_words_that_start_with_a_capital_letter = 0
    number_of_capital_letters = 0
    number_of_words = 0
    number_of_unknown_words = 0
    number_of_words_that_contain_dialectal_words = 0
    average_word_length = 0.0
    max_word_length = 0
    min_word_length = math.inf
    average_number_of_words_per_sentence = 0.0
    max_number_of_words_per_sentence = 0
    min_number_of_words_per_sentence = math.inf
    number_of_emojis = 0
    average_number_of_emojis_per_sentence = 0.0
    number_of_urls = 0
    number_of_question_marks = 0
    number_of_call_signs = 0
    number_of_dots = 0
    number_of_commas = 0
    number_of_digits = 0
    number_of_sarcasm_indicators = 0 # /s
    number_of_trigger_words = 0

    sentences = TextBlob(text).sentences
    number_of_sentences = 0
    for sentence in sentences:
        number_of_sentences = number_of_sentences + 1
        sentence = preprocessStrings(str(sentence))
        number_of_emojis = number_of_emojis +  len(re.findall(emoji_regex, sentence))
        number_of_urls = number_of_urls + len(re.findall(url_regex, sentence))
        number_of_question_marks = number_of_question_marks + len(re.findall("\?", sentence))
        number_of_call_signs = number_of_call_signs + len(re.findall("!", sentence))
        number_of_dots = number_of_dots + len(re.findall("\.", sentence))
        number_of_commas = number_of_commas + len(re.findall(",", sentence))
        number_of_digits = number_of_digits + len(re.findall("\d", sentence))
        number_of_sarcasm_indicators = number_of_sarcasm_indicators + len(re.findall("/s", sentence))
        words_of_sentence = TextBlob(sentence).words
        if len(words_of_sentence) > max_number_of_words_per_sentence:
            max_number_of_words_per_sentence = len(words_of_sentence)
        if len(words_of_sentence) < min_number_of_words_per_sentence:
            min_number_of_words_per_sentence = len(words_of_sentence)
        total_word_length = 0
        for word in words_of_sentence:
            total_word_length = total_word_length + len(word)
            if len(word) > max_word_length:
                max_word_length = len(word)
            if len(word) < min_word_length:
                min_word_length = len(word)
            number_of_words = number_of_words + 1
            number_of_unknown_words = number_of_unknown_words + checkIfWordIsKnown(word)
            for dialectal_regex in dialectal_regexes:
                if re.match(dialectal_regex, word.lower()):
                    number_of_words_that_contain_dialectal_words = number_of_words_that_contain_dialectal_words + 1
            for trigger_regex in trigger_regexes:
                if re.match(trigger_regex, word.lower()):
                    number_of_trigger_words = number_of_trigger_words + 1
            if word[0].isupper():
                number_of_words_that_start_with_a_capital_letter = number_of_words_that_start_with_a_capital_letter + 1
            for char in word:
                if char.isupper():
                    number_of_capital_letters = number_of_capital_letters + 1
    try:
        average_word_length = round(total_word_length / number_of_words,4)
        average_number_of_words_per_sentence = round(number_of_words / number_of_sentences, 4)
        average_number_of_emojis_per_sentence = round(number_of_emojis / number_of_sentences, 4)
    except: # Division by 0 error
        average_word_length = 0.0
        average_number_of_words_per_sentence = 0.0
        average_number_of_emojis_per_sentence = 0.0

    formatted_text = re.sub("\r|\n","    ",text)
    writer.writerow(["https://www.reddit.com/r/Austria/comments/" + submissionId + "/comment/" + commentId + "/",formatted_text,
                     number_of_words_that_start_with_a_capital_letter,number_of_capital_letters,number_of_words,
                     number_of_unknown_words,number_of_words_that_contain_dialectal_words,average_word_length,
                     max_word_length,min_word_length,average_number_of_words_per_sentence,
                     max_number_of_words_per_sentence,min_number_of_words_per_sentence,number_of_emojis,
                     average_number_of_emojis_per_sentence,number_of_urls,number_of_question_marks,number_of_call_signs,
                     number_of_dots,number_of_commas,number_of_digits,number_of_sarcasm_indicators,
                     number_of_trigger_words,upvotes,replies])

    return number_of_words_that_start_with_a_capital_letter, number_of_capital_letters, number_of_words, \
           number_of_unknown_words, number_of_words_that_contain_dialectal_words, average_word_length, \
           max_word_length, min_word_length, average_number_of_words_per_sentence, max_number_of_words_per_sentence, \
           min_number_of_words_per_sentence, number_of_emojis, average_number_of_emojis_per_sentence, number_of_urls, \
           number_of_question_marks, number_of_call_signs, number_of_dots, number_of_commas, number_of_digits, \
           number_of_sarcasm_indicators, number_of_trigger_words, upvotes, replies