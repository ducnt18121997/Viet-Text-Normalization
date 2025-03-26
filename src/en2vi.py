"""config:
1: Cách đọc theo anh - mĩ (US)
2: Cách đọc theo anh - anh (UK)
3: Cách đọc theo thuần việt (vie)
"""
from .modules.en2vi import *
from .config import list_vn_words, vn_charsets

def en2vi(istring: str) -> str:
    ostring = reading_teencode(istring)
    if ostring is not None:
        return ostring

    ostring = ""
    if istring in dict_en_words:
        ostring += dict_en_words[istring]
    elif istring.upper() in dict_en_chars:
        ostring += dict_en_chars[istring.upper()]
    elif "." in istring:
        ostring = " ".join(en2vi(w) for w in istring.split("."))
    else:
        if len(istring) <= 5 and \
                all(ch in vn_charsets.replace("|", "") for ch in istring) and \
                not any(ch in "aeiou" for ch in istring):
            ostring = " ".join([dict_en_chars[ch.upper()] for ch in istring])
        else:
            try:
                ostring = reading_english(istring)
            except:
                print(f"\t** \033[91m Errors en2vi \033[0m               : {istring}")
                pass

    return ostring


def reading_teencode(token: str) -> str:
    if token.startswith("z") and f"gi{token[1: ]}" in list_vn_words:
        return f"gi{token[1: ]}"
    
    return None


# Thứ tự ưu tiên: lemmatize sang dạng vietlish -> api2vi -> cmu2vi
def reading_english(istring: str) -> str:
    ostring = word_lemmatize(istring)
    if ostring is None:
        ostring = ipa2vi(istring)

    if ostring is None:
        ostring = cmu2vi(istring)

    return ostring
