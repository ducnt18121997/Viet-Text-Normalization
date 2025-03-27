import os
import json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class VietnameseWord:
    PATH = os.path.join(THIS_DIR, "dicts/words.txt")
    ### Vietnamese Word ###
    WORDS = open(PATH, "r", encoding="utf8").read().split("\n")
    PRONOUNS = [
        "cụ",
        "ông",
        "bà",
        "bác",
        "cô",
        "chú",
        "anh",
        "chị",
        "em",
        "cháu",
        "bé",
    ]


class VietnameseSpecialWord:
    READER = {
        "đắk": "đắc",
        "lắk": "lắc",
        "kạn": "cạn",
        "pưh": "pưn",
        "plông": "pờ lông",
        "kar": "car",
        "grai": "gờ rai",
        "búk": "búc",
        "păh": "păn",
        "jút": "giút",
        "kông": "công",
        "glong": "gờ long",
        "mil": "min",
        "chro": "chờ ro",
        "ayun": "ay un",
        "huoai": "hoai",
        "drai": "đờ rai",
        "v.v": "vân vân",
        "kbang": "cờ bang",
        "prông": "pờ rông",
        "pleiku": "pờ lây cu",
        "tẻh": "tẻn",
        "krông": "cờ rông",
        "kon": "con",
        "kuin": "cu in",
        "đrắk": "đờ rắc",
        "đăk": "đắc",
        "glei": "gờ lây",
        "mpú": "mờ pú",
    }


class VietnameseLocation:
    PATH = os.path.join(THIS_DIR, "dicts/static/location.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Vietnamese Location ###
    LOCATION = tuple(READER.keys())


class VietnameseArtist:
    PATH = os.path.join(THIS_DIR, "dicts/static/artist.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Vietnamese Artist ###
    ARTIST = tuple(READER.keys())


class VietnameseLoanWord:
    PATH = os.path.join(THIS_DIR, "dicts/static/loan.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Vietnamese Loan Word ###
    LOAN_WORD = tuple(READER.keys())


class VietnameseWebsite:
    PATH = os.path.join(THIS_DIR, "dicts/static/website.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Vietnamese Website ###
    WEBSITE = tuple(READER.keys())
    DOMAIN = {
        "com": "com",
        "vn": "vi-en",
        "org": "o-rờ-gờ",
        "net": "nét",
        "site": "sai",
        "top": "tốp",
        "tv": "tê-vê",
        "today": "tu-đây",
        "dev": "đép",
    }


class VietnameseMixWord:
    PATH = os.path.join(THIS_DIR, "dicts/static/mix.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Vietnamese Mix Word ###
    MIX_WORD = tuple(READER.keys())


class VietnameseBank:
    PATH = os.path.join(THIS_DIR, "dicts/static/bank.json")
    READER = json.load(open(PATH, "r", encoding="utf8"))
    ### Vietnamese Bank ###
    BANK = tuple(READER.keys())


class VietnameseAbbreviation:
    PATH = os.path.join(THIS_DIR, "dicts/static/")
    ### Vietnamese Abbreviation ###
    ModuleNotFoundError_ABBREVIATION = tuple(
        open(os.path.join(PATH, "mono.txt"), "r", encoding="utf8").read().split("\n")
    )
    DUO_ABBREVIATION = tuple(
        open(os.path.join(PATH, "duo.txt"), "r", encoding="utf8").read().split("\n")
    )
    START_DUO_ABBREVIATION = [x.split("#")[0] for x in DUO_ABBREVIATION]
    EXCEPTION_ABBREVIATION = tuple(
        open(os.path.join(PATH, "exception.txt"), "r", encoding="utf8")
        .read()
        .split("\n")
    )
