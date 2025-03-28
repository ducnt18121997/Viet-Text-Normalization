import re
from typing import List
from constants import charset, regular


def get_separator(string: str) -> str:
    if "/" in string:
        separator = "/"
    elif "-" in string:
        separator = "-"
    elif "." in string:
        separator = "."
    else:
        raise TypeError(f"Unidentify separator, given string: {string}")

    return separator


def split_num_word(token: str) -> str:
    token = re.sub(
        r"(?P<id>(\d[{}]))".format(charset.VietnameseCharset.CHARSETS),
        lambda x: x.group("id")[0] + " " + x.group("id")[1],
        token,
    )
    token = re.sub(
        r"(?P<id>([{}]\d))".format(charset.VietnameseCharset.CHARSETS),
        lambda x: x.group("id")[0] + " " + x.group("id")[1],
        token,
    )

    token = re.sub(
        r"(?P<id>(\d\D))", lambda x: x.group("id")[0] + " " + x.group("id")[1], token
    )
    token = re.sub(
        r"(?P<id>(\d\D))".format(charset.VietnameseCharset.CHARSETS),
        lambda x: x.group("id")[0] + " " + x.group("id")[1],
        token,
    )

    return token


def split_punc_char(token: str) -> str:
    # tách dấu đi liền với từ
    token = re.sub(
        r"(?P<id>[{}])(?P<id1>{})(?P<id2>[{}])".format(
            charset.VietnameseCharset.CHARSETS,
            regular.PunctuationRegular.PUNCTUATION,
            charset.VietnameseCharset.CHARSETS,
        ),
        lambda x: x.group("id") + " " + x.group("id1") + " " + x.group("id2"),
        token,
    )
    token = re.sub(
        r"(?P<id>[{}])(?P<id1>{})(?P<id2>[{}])".format(
            charset.VietnameseCharset.CHARSETS,
            regular.PunctuationRegular.PUNCTUATION,
            charset.VietnameseCharset.CHARSETS,
        ),
        lambda x: x.group("id") + " " + x.group("id1") + " " + x.group("id2"),
        token,
    )

    token = re.sub(
        r"(?P<id>[{}])(?P<id1>{})(?P<id2>\d)".format(
            "-", charset.VietnameseCharset.CHARSETS
        ),
        lambda x: x.group("id") + " " + x.group("id2"),
        token,
    )
    token = re.sub(
        r"(?P<id>[{}])(?P<id1>{})(?P<id2>\d)".format(
            charset.VietnameseCharset.CHARSETS, "-"
        ),
        lambda x: x.group("id") + " " + x.group("id2"),
        token,
    )

    token = re.sub(
        r"(?P<id>\d)(?P<id1>{})(?P<id2>{})".format(
            regular.PunctuationRegular.PUNCTUATION, charset.VietnameseCharset.CHARSETS
        ),
        lambda x: x.group("id") + " " + x.group("id1") + " " + x.group("id2"),
        token,
    )
    token = re.sub(
        r"(?P<id>{})(?P<id1>{})(?P<id2>\d)".format(
            charset.VietnameseCharset.CHARSETS,
            regular.PunctuationRegular.PUNCTUATION,
        ),
        lambda x: x.group("id") + " " + x.group("id1") + " " + x.group("id2"),
        token,
    )

    token = re.sub(
        r"(?P<id>{})(?P<id1>{})".format(
            regular.PunctuationRegular.PUNCTUATION,
            charset.VietnameseCharset.CHARSETS,
        ),
        lambda x: x.group("id") + " " + x.group("id1"),
        token,
    )
    token = re.sub(
        r"(?P<id>{})(?P<id1>{})".format(
            charset.VietnameseCharset.CHARSETS,
            regular.PunctuationRegular.PUNCTUATION,
        ),
        lambda x: x.group("id") + " " + x.group("id1"),
        token,
    )

    return token


def is_number(istring: str, lst_sep: List = [",", "."]) -> bool:

    return all(ch.isdigit() or ch in lst_sep for ch in istring)


def is_short_name(istring: str):

    return istring.isupper() and all(
        len(ch) == 1 for ch in istring.replace(".", " ").split()
    )
