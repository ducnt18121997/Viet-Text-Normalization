import os
import json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class VietnameseCharset:
    PATH = os.path.join(THIS_DIR, "dicts/characters.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Lowercase ###
    LOWER_VOWELS = "a|á|ả|à|ã|ạ|â|ấ|ẩ|ầ|ẫ|ậ|ă|ắ|ẳ|ằ|ẵ|ặ|e|é|ẻ|è|ẽ|ẹ|ê|ế|ể|ề|ễ|ệ|i|í|ỉ|ì|ĩ|ị|o|ó|ỏ|ò|õ|ọ|ô|ố|ổ|ồ|ỗ|ộ|ơ|ớ|ở|ờ|ỡ|ợ|u|ú|ủ|ù|ũ|ụ|ư|ứ|ử|ừ|ữ|ự|y|ý|ỷ|ỳ|ỹ|ỵ"
    LOWER_CONSONANTS = "b|c|d|đ|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z"
    LOWER_CHARSETS = LOWER_VOWELS + "|" + LOWER_CONSONANTS
    ### Uppercase ###
    UPPER_VOWELS = "A|Á|Ả|À|Ã|Ạ|Â|Ấ|Ẩ|Ầ|Ẫ|Ậ|Ă|Ắ|Ẳ|Ằ|Ẵ|Ặ|E|É|Ẻ|È|Ẽ|Ẹ|Ê|Ế|Ể|Ề|Ễ|Ệ|I|Í|Ỉ|Ì|Ĩ|Ị|O|Ó|Ỏ|Ò|Õ|Ọ|Ô|Ố|Ổ|Ồ|Ỗ|Ộ|Ơ|Ớ|Ở|Ờ|Ỡ|Ợ|U|Ú|Ủ|Ù|Ũ|Ụ|Ư|Ứ|Ử|Ừ|Ữ|Ự|Y|Ý|Ỷ|Ỳ|Ỹ|Ỵ"
    UPPER_CONSONANTS = "B|C|D|Đ|F|G|H|J|K|L|M|N|P|Q|R|S|T|V|W|X|Z"
    UPPER_CHARSETS = UPPER_VOWELS + "|" + UPPER_CONSONANTS
    ### General ###
    CHARSETS = LOWER_CHARSETS + "|" + UPPER_CHARSETS
    ONLY_CHARSETS = "á|ả|à|ã|ạ|â|ấ|ẩ|ầ|ẫ|ậ|ă|ắ|ẳ|ằ|ẵ|ặ|é|ẻ|è|ẽ|ẹ|ê|ế|ể|ề|ễ|ệ|í|ỉ|ì|ĩ|ị|ó|ỏ|ò|õ|ọ|ô|ố|ổ|ồ|ỗ|ộ|ơ|ớ|ở|ờ|ỡ|ợ|ú|ủ|ù|ũ|ụ|ư|ứ|ử|ừ|ữ|ự|ý|ỷ|ỳ|ỹ|ỵ"
    DOUBLE_CONSONANTS = "ch|ng|nh|ph|qu|th|tr"
    TONE_FORMAT = {
        "òa": "oà",
        "óa": "oá",
        "ọa": "oạ",
        "õa": "oã",
        "ỏa": "oả",
        "òe": "oè",
        "óe": "oé",
        "ọe": "oẹ",
        "õe": "oẽ",
        "ỏe": "oẻ",
        "ùy": "uỳ",
        "úy": "uý",
        "ụy": "uỵ",
        "ũy": "uỹ",
        "ủy": "uỷ",
        "Òa": "Oà",
        "Óa": "Oá",
        "Ọa": "Oạ",
        "Õa": "Oã",
        "Ỏa": "Oả",
        "Òe": "Oè",
        "Óe": "Oé",
        "Ọe": "Oẹ",
        "Õe": "Oẽ",
        "Ỏe": "Oẻ",
        "Òy": "Uỳ",
        "Úy": "Uý",
        "Ụy": "Uỵ",
        "Ũy": "Oỹ",
        "Ủy": "Uỷ",
    }


class EnglishCharset:
    CONSONANTS = "b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z"
    VOWELS = "a|e|o|u|i"
    CHARSETS = VOWELS + "|" + CONSONANTS
    ONLY_CHARSETS = "j|f|w|z"


class SymbolCharset:
    PATH = os.path.join(THIS_DIR, "dicts/static/symbol.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Symbol ###
    SYMBOL = list(READER.keys())


class PunctuationCharset:
    PATH = os.path.join(THIS_DIR, "dicts/static/punctuation.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Punctuation ###
    PUNCTUATION = list(READER.keys())
    ### Special ###
    SKIP = ["'", """, """, """, """, "*", "…", ")", "]", "}", "~", "`", "_"]
    SILENT = [".", ",", ";", "!", "-", "?", ":", "(", "[", "{"]
    DURATION = SKIP + SILENT
    READ = []
    for punc in PUNCTUATION:
        if punc not in DURATION:
            READ.append(punc)


class UnitCharset:
    PATH = os.path.join(THIS_DIR, "dicts/unit/base.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Unit ###
    UNIT = list(sorted(list(READER.keys()), key=lambda x: len(x), reverse=True))


class CurrencyCharset:
    PATH = os.path.join(THIS_DIR, "dicts/unit/currency.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Currency ###
    CURRENCY = list(READER.keys())


class RomanCharset:
    READER = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
        "IV": 4,
        "IX": 9,
        "XL": 40,
        "XC": 90,
        "CD": 400,
        "CM": 900,
    }
