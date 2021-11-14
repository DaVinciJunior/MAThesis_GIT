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

unknown_words = []

def addWord(word):
    # only add word if consists of following regex - otherwise it is just a random character, number, ...
    if re.fullmatch(pattern="((\d)*([a-z]|[A-Z]|[äöü]|[ÄÖÜ]|[é])+(\S)*)+", string=word):
        unknown_words.append(word)

def log():
    # Remove duplicates via set()
    # Initialize lower unknown words
    unknown_words_lower = set([unknown_word.lower() for unknown_word in unknown_words])
    for word in unknown_words_lower:
        logger.info(word)