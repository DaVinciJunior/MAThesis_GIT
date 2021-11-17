import logging
import os
import re

from datetime import datetime

path_to_logs = 'B:\\Dropbox\\MA\\GIT\\logs'

today = datetime.now()
formated_today = today.strftime('%d_%m_%Y_%H_%M')

dir_path = path_to_logs
filename = os.path.join(dir_path, formated_today + '.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename, "a", "utf-8")
file_handler.setLevel(logging.INFO)
#file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

unknown_words = {}
possible_mappings = {}

def addWord(word):
    # only add word if consists of following regex - otherwise it is just a random character, number, ...
    if re.fullmatch(pattern="((\d)*([a-z]|[A-Z]|[äöü]|[ÄÖÜ]|[é])+(\S)*)+", string=word):
        word = word.lower()
        if word in unknown_words.keys():
            unknown_words[word] = unknown_words[word] + 1
        else:
            unknown_words[word] = 1

def addPossibleMapping(word, mapping):
    removeUnknownWordsBecauseOfMatch(word)

    word = word.lower()
    if word in possible_mappings.keys():
        possible_mappings[word].add(mapping)
    else:
        possible_mappings[word] = {mapping}


def removeUnknownWordsBecauseOfMatch(word):
    # If we have at least one mapping for a word we remove it from the possible dialectal words
    if word in unknown_words.keys():
        del unknown_words[word]


def log():
    # Remove duplicates via set()
    # Initialize lower unknown words
    logger.info("------------------\nAll unknown words\n------------------")
    for word in unknown_words.keys():
        logger.info(word + ":" + str(unknown_words[word]))
    logger.info("------------------\nDialectal Mappings\n------------------")
    for word in possible_mappings.keys():
        logger.info(word + "->" + str(possible_mappings[word]))