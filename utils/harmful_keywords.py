# CronusMainframe/utils/harmful_keywords.py

import os
import re

def load_harmful_keywords(directory):
    harmful_keywords = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                harmful_keywords.extend(line.strip() for line in file)
    return harmful_keywords

def add_word_boundaries(keywords):
    return [r'\b' + re.escape(keyword) + r'\b' for keyword in keywords]

HARMFUL_KEYWORDS = add_word_boundaries(load_harmful_keywords('utils/keywords'))
