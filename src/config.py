# -*- coding: utf-8 -*-
import os
import json


####################################################################################
############################### VIETNAMESE CHARSET #################################
####################################################################################
vn_lower_vowels      = "a|á|ả|à|ã|ạ|â|ấ|ẩ|ầ|ẫ|ậ|ă|ắ|ẳ|ằ|ẵ|ặ|e|é|ẻ|è|ẽ|ẹ|ê|ế|ể|ề|ễ|ệ|i|í|ỉ|ì|ĩ|ị|o|ó|ỏ|ò|õ|ọ|ô|ố|ổ|ồ|ỗ|ộ|ơ|ớ|ở|ờ|ỡ|ợ|u|ú|ủ|ù|ũ|ụ|ư|ứ|ử|ừ|ữ|ự|y|ý|ỷ|ỳ|ỹ|ỵ"
vn_lower_consonants  = "b|c|d|đ|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z"
vn_lower_charsets    = vn_lower_vowels + "|" + vn_lower_consonants
vn_upper_vowels      = "A|Á|Ả|À|Ã|Ạ|Â|Ấ|Ẩ|Ầ|Ẫ|Ậ|Ă|Ắ|Ẳ|Ằ|Ẵ|Ặ|E|É|Ẻ|È|Ẽ|Ẹ|Ê|Ế|Ể|Ề|Ễ|Ệ|I|Í|Ỉ|Ì|Ĩ|Ị|O|Ó|Ỏ|Ò|Õ|Ọ|Ô|Ố|Ổ|Ồ|Ỗ|Ộ|Ơ|Ớ|Ở|Ờ|Ỡ|Ợ|U|Ú|Ủ|Ù|Ũ|Ụ|Ư|Ứ|Ử|Ừ|Ữ|Ự|Y|Ý|Ỷ|Ỳ|Ỹ|Ỵ"
vn_upper_consonants  = "B|C|D|Đ|F|G|H|J|K|L|M|N|P|Q|R|S|T|V|W|X|Z"
vn_upper_charsets    = vn_upper_vowels + "|" + vn_upper_consonants
vn_charsets          = vn_lower_charsets + "|" + vn_upper_charsets
vn_only_charsets     = "á|ả|à|ã|ạ|â|ấ|ẩ|ầ|ẫ|ậ|ă|ắ|ẳ|ằ|ẵ|ặ|é|ẻ|è|ẽ|ẹ|ê|ế|ể|ề|ễ|ệ|í|ỉ|ì|ĩ|ị|ó|ỏ|ò|õ|ọ|ô|ố|ổ|ồ|ỗ|ộ|ơ|ớ|ở|ờ|ỡ|ợ|ú|ủ|ù|ũ|ụ|ư|ứ|ử|ừ|ữ|ự|ý|ỷ|ỳ|ỹ|ỵ"
vn_double_consonants = "ch|ng|nh|ph|qu|th|tr" 
vn_tone_format       = {
    "òa": "oà", "óa": "oá", "ọa": "oạ", "õa": "oã", "ỏa": "oả",
    "òe": "oè", "óe": "oé", "ọe": "oẹ", "õe": "oẽ", "ỏe": "oẻ",
    "ùy": "uỳ", "úy": "uý", "ụy": "uỵ", "ũy": "uỹ", "ủy": "uỷ",
    "Òa": "Oà", "Óa": "Oá", "Ọa": "Oạ", "Õa": "Oã", "Ỏa": "Oả",
    "Òe": "Oè", "Óe": "Oé", "Ọe": "Oẹ", "Õe": "Oẽ", "Ỏe": "Oẻ",
    "Òy": "Uỳ", "Úy": "Uý", "Ụy": "Uỵ", "Ũy": "Oỹ", "Ủy": "Uỷ"
}

####################################################################################
############################### ENGLISH CHARSET ####################################
####################################################################################
en_consonants        = "b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z"
en_vowels            = "a|e|o|u|i"
en_charsets          = en_vowels + "|" + en_consonants
en_only_charsets     = "j|f|w|z"

####################################################################################
############################### EMAIL/URL REGREX ###################################
####################################################################################
email_regex          = r"[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4})+"
full_url             = r"((?:http(s)?:\/\/)|(www))[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\"\(\)\*\+,;=.]+"
short_url            = r"([\w.-]+(?:\.[\w\.-]+)+)?[\w\-\._~:/?#[\]@!\$&\"\(\)\*\+,;=.]+(\.(com|gov|vn|com|org|info|io|net|edu))+"
url_regex            = "|".join([full_url, short_url])

####################################################################################
############################### SPECIAL SYMBOLES (α, ξ) ############################
####################################################################################
dict_symbol          = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/static/symbol.json"), "r"))
re_symbol            = "|".join(list(dict_symbol.keys()))

####################################################################################
############################### PUNCTUATION DICTIONARY #############################
####################################################################################
dict_punc            = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/static/punctuation.json"), "r"))
list_punc            = list(dict_punc.keys())
list_punc_skip       = ["‘", """, """, "“", "”", "*", "…", ")", "]", "}", "~", "`", "_"]
list_punc_silent     = [".", ",", ";", "!", "-", "?", ":", "(", "[", "{"] 
list_punc_dura       = list_punc_skip + list_punc_silent
list_punc_read       = [punc for punc in list_punc if punc not in list_punc_dura]
re_punc_read         = "|\\".join(list_punc_dura)
re_punc_dura         = "|\\".join(list_punc_read)
re_punc              = re_punc_read + "|" + re_punc_dura

####################################################################################
############################### VIETNAMESE DICTIONARY ##############################
####################################################################################
list_vn_words       = open(os.path.join(os.path.dirname(__file__), "dicts/words.txt"), "r", encoding="utf8").read().split("\n")
dict_vn_chars       = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/characters.json"), "r"))
dict_vn_words       = dict.fromkeys(list_vn_words, 0)
dict_spec_words     = {
    "đắk": "đắc", "lắk": "lắc", "kạn": "cạn", "pưh": "pưn", "plông": "pờ lông", "kar": "car",
    "grai": "gờ rai", "búk": "búc", "păh": "păn", "jút": "giút", "kông": "công", "glong": "gờ long",
    "mil": "min", "chro": "chờ ro", "ayun": "ay un", "huoai": "hoai", "drai": "đờ rai", "v.v": "vân vân",
    "kbang": "cờ bang", "prông": "pờ rông", "pleiku": "pờ lây cu", "tẻh": "tẻn", "krông": "cờ rông",
    "kon": "con", "kuin": "cu in", "đrắk": "đờ rắc", "đăk": "đắc", "glei": "gờ lây", "mpú": "mờ pú"
}
list_vn_pronouns    = ["cụ", "ông", "bà", "bác", "cô", "chú", "anh", "chị", "em", "cháu", "bé"]
dict_vn_location    = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/static/location.json"), "r"))
list_vn_location    = tuple([f"{w}." for w in dict_vn_location.keys()])
dict_artist         = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/static/artist.json"), "r"))
dict_loan_words     = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/static/loan.json"), "r"))
dict_website_name   = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/static/website.json"), "r"))
dict_website_domain = {
    "com": "com", "vn": "vi-en", "org": "o-rờ-gờ", "net": "nét", "site": "sai", "top": "tốp", "tv": "tê-vê",
    "today": "tu-đây", "dev": "đép"
}
list_website_domain = tuple([f".{w}" for w in dict_website_domain.keys()])
dict_mix_words      = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/static/mix.json"), "r"))
dict_bank           = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/static/bank.json"), "r"))

####################################################################################
############################### UNITS DICTIONARY ###################################
####################################################################################
dict_base_unit      = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/unit/base.json"), "r"))
list_base_unit      = tuple(sorted(list(dict_base_unit.keys()), key=lambda x: len(x), reverse=True))
dict_currency_unit  = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/unit/currency.json"), "r"))

####################################################################################
############################### ABB DICTIONARY #####################################
####################################################################################
dict_exception_abb  = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/abb/exception.json"), "r"))
dict_mono_abb       = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/abb/mono.json"), "r"))
dict_duo_abb        = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/abb/duo.json"), "r"))
list_start_duo_abb  = [x.split("#")[0] for x in dict_duo_abb.keys()]
####################################################################################
