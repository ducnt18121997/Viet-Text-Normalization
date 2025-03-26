""" thư viện đọc NSWs dạng chữ sang tiếng việt """
import re
import unidecode
import unicodedata
from typing import List

from .config import *
from .modules.reading import *
from .en2vi import dict_en_common_words, en2vi


def UPPER2words(istring: str, read_dict: bool=True) -> str:
    # đọc từ điển mapping từ viết tất
    if read_dict is True and istring in dict_mono_abb:
        ostring = dict_mono_abb[istring]
    # đọc từ điển mapping từ viết hoa đọc bình thường
    elif istring in dict_exception_abb:
        ostring = dict_exception_abb[istring]
    # đọc theo tiếng việt
    elif istring.lower() in list_vn_words:
        ostring = istring.lower()
    # đọc theo từ tiếng anh thông dụng
    elif istring.lower() in dict_en_common_words:
        ostring = dict_en_common_words[istring.lower()]
    elif "." in istring:
        istring = unidecode.unidecode(istring).replace(".", " ").strip().split()
        ostring = " ".join([UPPER2words(s) for s in istring])
    # đọc từ UPPER ko xác định
    else:
        if len(istring) <= 6 or "Ư" in istring or all(s not in "AEOIU".upper() for s in istring):
            ostring = " ".join([dict_vn_chars[ch] for ch in istring if ch in dict_vn_chars])       
        else:
            ostring = LOWER2words(istring.lower())

    return ostring


def LOWER2words(istring: str) -> str:
    if istring.endswith("."): # maybe <EOS>
        return f" {LOWER2words(istring[: -1])} {istring[-1]} "
    if "-" in istring: 
        return " ".join([LOWER2words(x) for x in istring.split("-") if x])
    # dọc tên ngân hàng (bank)
    elif istring.endswith("bank"):
        ostring = f"{LOWER2words(istring[: -4])} banh"
    # đọc từ tiếng anh default
    else:
        ostring = en2vi(unicodedata.normalize('NFD', istring).encode('ascii', 'ignore').decode())

    return ostring


def NUMBER2words(istring: str) -> str:
    if istring.endswith("."): # maybe <EOS>
        return f" {NUMBER2words(istring[: -1])} {istring[-1]} "
    elif "+" in istring or istring.startswith("-"):
        ostring = f" {'cộng' if istring[0] == '+' else 'trừ'} {NUMBER2words(istring[1: ])} "
    elif isNumber(istring, [".", ","]):
        _string = istring.replace("+", " cộng ").replace("-", " trừ ").split()
        ostring = " ".join([read_nnumber(x) if x not in ["cộng", "trừ"] else x for x in _string])
    elif "-" in istring or ":" in istring:
        _string = istring.replace("-", " ").replace(":", " ").split()
        ostring = " ".join([NUMBER2words(x) for x in _string])
    elif "/" in istring:
        if re.fullmatch(r"\b(2[0-4]|1[0-9]|0?[1-9])\/(1[0-2]|0?[1-9])\b", istring):
            ostring = read_nday(istring)
        elif re.fullmatch(r"\b(1[0-2]|0?[1-9])\/([12]\d{3})\b", istring):
            ostring = read_nmon(istring)
        else:
            _string = istring.split("/")
            ostring = " trên ".join(NUMBER2words(_str) for _str in _string if _str)
    elif istring[-1] in dict_currency_unit:
        ostring = f"{read_nnumber(istring[: -1])} {dict_currency_unit[istring[-1]]}"
    elif istring[0] in dict_currency_unit:
        ostring = f"{read_nnumber(istring[1: ])} {dict_currency_unit[istring[0]]}"
    elif istring in dict_base_unit:
        ostring = dict_base_unit[istring]
    else:
        _string = splitNumWor(istring).split()
        ostring = []
        for x in _string:
            if x.isdigit():
                ostring.append(read_nnumber(x) if x[0] != "0" else read_ndigit(x))
            elif x.lower() in list_vn_words:
                ostring.append(x.lower())
            elif x.isupper():
                ostring.append(UPPER2words(x, read_dict=False))
            else:
                ostring.append(LOWER2words(x))
        ostring = " ".join(ostring)

    return ostring


def isNumber(istring: str, lst_sep: List=[",", "."]) -> bool:
    
    return all(ch.isdigit() or ch in lst_sep for ch in istring)


def splitNumWor(token: str) -> str:
    token = re.sub(r"(?P<id>(\d[{}]))".format(vn_charsets),
        lambda x: x.group("id")[0] + " " + x.group("id")[1], token)
    token = re.sub(r"(?P<id>([{}]\d))".format(vn_charsets),
        lambda x: x.group("id")[0] + " " + x.group("id")[1], token)
    
    token = re.sub(r"(?P<id>(\d\D))",
        lambda x: x.group("id")[0] + " " + x.group("id")[1], token)
    token = re.sub(r"(?P<id>(\d\D))".format(vn_charsets),
        lambda x: x.group("id")[0] + " " + x.group("id")[1], token)

    return token


def splitPuncChar(token: str) -> str:
    # tách dấu đi liền với từ
    token = re.sub(r"(?P<id>[{}])(?P<id1>{})(?P<id2>[{}])".format(vn_charsets, re_punc, vn_charsets),
        lambda x: x.group("id") + " " + x.group("id1") + " " + x.group("id2"), token)
    token = re.sub(r"(?P<id>[{}])(?P<id1>{})(?P<id2>[{}])".format(vn_charsets, re_punc, vn_charsets),
        lambda x: x.group("id") + " " + x.group("id1") + " " + x.group("id2"), token)

    token = re.sub(r"(?P<id>[{}])(?P<id1>{})(?P<id2>\d)".format("-", vn_charsets),
        lambda x: x.group("id") + " " + x.group("id2"), token)
    token = re.sub(r"(?P<id>[{}])(?P<id1>{})(?P<id2>\d)".format(vn_charsets, "-"),
        lambda x: x.group("id") + " " + x.group("id2"), token)

    token = re.sub(r"(?P<id>\d)(?P<id1>{})(?P<id2>{})".format(re_punc, vn_charsets),
        lambda x: x.group("id") + " " + x.group("id1") + " " + x.group("id2"), token)
    token = re.sub(r"(?P<id>{})(?P<id1>{})(?P<id2>\d)".format(vn_charsets, re_punc),
        lambda x: x.group("id") + " " + x.group("id1") + " " + x.group("id2"), token)

    token = re.sub(r"(?P<id>{})(?P<id1>{})".format(re_punc, vn_charsets),
        lambda x: x.group("id") + " " + x.group("id1"), token)
    token = re.sub(r"(?P<id>{})(?P<id1>{})".format(vn_charsets, re_punc),
        lambda x: x.group("id") + " " + x.group("id1"), token)

    return token


def isShortName(istring: str):
    
    return istring.isupper() and all(len(ch) == 1 for ch in istring.replace(".", " ").split())

    