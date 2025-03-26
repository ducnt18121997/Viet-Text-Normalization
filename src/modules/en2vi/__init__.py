import os
import glob
import json
import unidecode
from .api2vi import ipa2vi
from .cmu2vi import cmu2vi


############################### ENGLISH DICTIONARY #################################
dict_en_chars        = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/characters.json"), "r"))
dict_en_common_words = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/common_words.json"), "r"))
dict_en_common_words.update(json.load(open(os.path.join(os.path.dirname(__file__), "dicts/verified_words.json"), "r"))) # add verified english words to common_words (no need to change code)
dict_en_words        = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/words.json"), "r"))
dict_en_words.update(dict_en_common_words.copy())
for dict_name in glob.glob(os.path.join(os.path.dirname(__file__), "dicts/static/*.json")):
    dict_en_words.update(json.load(open(dict_name, "r")))
dict_confuse_words  = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/static/confuse.json"), "r"))
reading_prefixes     = {"un":"ăn", "in":"in", "im":"im", "il":"i", "ir":"i", "dis":"đít", "non":"năn", "over":"âu-vờ", "super":"súp-pơ", "re":"ri", "mis":"mít", "pre":"pờ-ri", "mono":"mô-nô", "bi":"bi", "tri":"tri", "multi":"mu-ti"}
reading_suffixes     = {"dom":"đừm", "ment":"mừn", "ness":"nít", "sion":"sừn", "tion":"sừn", "ship":"síp", "ful":"phu", "less":"lớt", "ly":"ly", "ward":"guốt", "wards":"guốt", "wise":"goai", "ty":"ty", "fy":"phai"}
reading_v_suffixes   = {"acy":"ơ-si", "ance":"ừn-sờ", "ence":"ừn-sờ", "ity":"i-ty", "al":"ồ", "or":"ờ", "ist":"ít", "ism":"i-sừm", "ate":"ết", "en":"ừn", "ify":"i-phai", "ise":"ai", "ize":"ai", "able":"ơ-bồ", "ible":"ơ-bồ", "esque":"ét-cờ", "ive":"íp", "ic":"ích", "ical":"i-cồ", "ious":"ợt", "ous":"ớt", "ish":"ít"}
##############################################################################0######
####################################################################################


def word_lemmatize(eng_string: str) -> str:
    # Check tiền tố của từ tiếng anh
    prefix = sorted([k for k in reading_prefixes if eng_string.startswith(k)], \
        key=lambda x: len(x), reverse=True)

    if len(prefix) > 0:
        prefix = prefix[0]
        cutted_word = eng_string[len(prefix): ]
        if cutted_word in dict_en_common_words:

            return f"{reading_prefixes[prefix]}-{dict_en_common_words[cutted_word]}"
        else:
            # Check hậu tố của từ tiếng anh
            cutted_word = check_suffix(cutted_word)
            if cutted_word is not None:

                return f"{reading_prefixes[prefix]}-{cutted_word}"

    # NOTE: nếu như ko thẻ tìm được hậu tố thì sẽ trả lại từ ban đầu để xử lý
    return None


# Check hậu tố của từ tiếng anh
def check_suffix(word: str) -> str:
    # tách hậu tố bắt đầu bằng coda
    suffix = sorted([k for k in reading_suffixes if word.endswith(k)], \
        key=lambda x: len(x), reverse=True)
    if len(suffix) > 0:
        suffix = suffix[0]
        cutted_word = word[: -len(suffix)]

        if f"{cutted_word}e" in dict_en_common_words:
            
            return dict_en_common_words[f"{cutted_word}e"] + "-" + reading_suffixes[suffix]
        elif f"{cutted_word[:-1]}y" in dict_en_common_words:
            
            return dict_en_common_words[f"{cutted_word[:-1]}y"] + "-" + reading_suffixes[suffix]
        elif cutted_word in dict_en_common_words:
            
            return dict_en_common_words[cutted_word] + "-" + reading_suffixes[suffix]

    # tách hậu tố bắt đầu bằng vowel
    suffix = sorted([k for k in reading_v_suffixes if word.endswith(k)], \
        key=lambda x: len(x), reverse=True)
    if len(suffix) > 0:
        suffix = suffix[0]
        cutted_word = word[: -len(suffix)]
        if cutted_word in dict_en_common_words:
            # Trường hợp từ = english word + tail

            return dict_en_common_words[cutted_word] + "-" + suffix2vi(cutted_word, suffix)
        elif f"{cutted_word}e" in dict_en_common_words:
            # Trường hợp từ = english word (thiếu "e") + tail

            return dict_en_common_words[f"{cutted_word}e"] + "-" + suffix2vi(cutted_word, suffix)

    return None


def suffix2vi(cutted_word, suffix):
    if cutted_word.endswith("d"):
        tail = "đ" + reading_v_suffixes[suffix]
    elif cutted_word.endswith("sh"):
        tail = "s" + reading_v_suffixes[suffix]
    elif cutted_word.endswith("k"):
        tail = reading_v_suffixes[suffix]
        if unidecode.unidecode(tail).startswith(("i", "e")):
            tail = "k" + reading_v_suffixes[suffix]
        else:
            tail = "c" + reading_v_suffixes[suffix]
    elif cutted_word.endswith("c"):
        tail = "s" + reading_v_suffixes[suffix]
    else:
        tail = reading_v_suffixes[suffix]

    return tail
