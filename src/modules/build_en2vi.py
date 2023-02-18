import os
import json
import string
import pronouncing

from tqdm import tqdm
from en2vi import *


if __name__ == "__main__":
    english_words = pronouncing.cmudict.words()
    vietnamese_words = []
    for en_word in tqdm(english_words):
        if any(ch not in string.ascii_lowercase for ch in en_word) or len(en_word) < 2:
            continue
            
        if not any(ch in ["a", "e", "i", "o", "u"] for ch in en_word):
            continue
        
        vi_word = word_lemmatize(en_word)
        if vi_word == None:
            vi_word = ipa2vi(en_word)
        if vi_word == None:
            vi_word = cmu2vi(en_word)

        vietnamese_words.append([en_word, vi_word])

    vietnamese_words = {k: v for k, v in sorted(vietnamese_words, key= lambda x: x[0])}
    with open(os.path.join(os.path.dirname(__file__), "en2vi/dicts/words.json"), "w", encoding="utf8") as f:
        json.dump(vietnamese_words, f, ensure_ascii=False, indent=4)