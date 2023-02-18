import re
from src.config import *


def split_compound_nsw(input_txts: str) -> str:
    list_tokens = []
    for i, token in enumerate(input_txts.split()):
        if i == 0 and token in ["-", "+"]:
            continue
        elif token.lower() in list_vn_words:
            list_tokens.append(token.lower())
        # Xử lý các từ tiếng việt được ghép nối bởi lỗi hoặc từ 1st normalization
        elif "-" in token and all(w in list_vn_words for w in token.split("-")):
            list_tokens.append(token.replace("-", " "))
        # Xử lý trường hợp tên người bị nối liền
        elif token != "." and all(c in (vn_upper_charsets + ".") for c in token):
            list_tokens.append(token.replace(".", " "))
        else:
            # phân tách ký tự đặc biệt
            token = re.sub(r"(?P<id>{})".format(re_symbol),
                lambda x: " " + x.group("id") + " ", token)

            # tách tên
            if token.isupper():
                token = re.sub(r"(?P<id>[{}])(?P<id1>{})(?P<id2>[{}])".format(vn_charsets, "-", vn_charsets),
                    lambda x: x.group("id") + " - " + x.group("id2"), token)
            else:
                token = re.sub(r"(?P<id>[{}])(?P<id1>{})(?P<id2>[{}])".format(vn_charsets, "-", vn_charsets),
                                lambda x: x.group("id") + " " + x.group("id2"), token)

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

            # Tách số đi liền với từ
            if token != token.upper():
                token = re.sub(r"(?P<id>(\d[{}]))".format(vn_charsets),
                    lambda x: x.group("id")[0] + " " + x.group("id")[1], token)
                token = re.sub(r"(?P<id>([{}]\d))".format(vn_charsets),
                    lambda x: x.group("id")[0] + " " + x.group("id")[1], token)
            else:
                token = re.sub(r"(?P<id>(\d[{}]))".format(vn_charsets),
                    lambda x: x.group("id")[0] + " " + x.group("id")[1], token)
                token = re.sub(r"(?P<id>([{}]\d))".format(vn_charsets),
                    lambda x: x.group("id")[0] + " " + x.group("id")[1], token)

            # tách các punctuation liền nhau
            token = re.sub(r"(?P<id>{})(?P<id1>{})".format(re_punc, re_punc),
                lambda x: x.group("id") + " " + x.group("id1"), token)
            token = re.sub(r"(?P<id>{})(?P<id1>{})".format(re_punc, re_punc),
                lambda x: x.group("id") + " " + x.group("id1"), token)

            list_tokens.append(token)

    return " ".join(list_tokens)


def tokenize_nsw(text):
    # Tách dấu (trừ với dấu . và , tách theo dạng khác) và không tách dấu -
    text = re.sub(r"(?P<id>{})\s+".format("\.|\,|"),
                  lambda x: " " + x.group("id") + " ", text)
    text = re.sub(r"(?P<id>{})".format(re_punc.replace(("|\-"), "").replace("\.|\,|", "")),
                  lambda x: " " + x.group("id") + " ", text)

    # 2/ 3, 2 /3, 2 / 3 => 2/3
    text = re.sub(r"(?P<id>\d+)(\s+\/|\/\s+|\s+\/\s+)(?P<id1>\d+)",
                  lambda x: x.group("id") + "/" + x.group("id1"), text)
    text = re.sub(r"(?P<id>\d+)(\s+\/|\/\s+|\s+\/\s+)(?P<id1>\d+)",
                  lambda x: x.group("id") + "/" + x.group("id1"), text)

    # 30- 40, 30 -40, 30 - 40 => 30-40
    text = re.sub(r"(?P<id>\d+)(\s+\-|\-\s+|\s+\-\s+)(?P<id1>\d+)",
                  lambda x: x.group("id") + "-" + x.group("id1"), text)
    text = re.sub(r"(?P<id>\d+)(\s+\-|\-\s+|\s+\-\s+)(?P<id1>\d+)",
                  lambda x: x.group("id") + "-" + x.group("id1"), text)

    # 30 % => 30%
    text = re.sub(r"(?P<id>\d+)(\s+\%)",
                  lambda x: x.group("id") + "%", text)
    text = re.sub(r"(?P<id>\d+)(\s+\%)",
                  lambda x: x.group("id") + "%", text)

    # 2 : 30 => 2:30, 12 : 30 : 59 => 12:30:59
    text = re.sub(r"(?P<id>\d+)(\s+\:|\:\s+|\s+\:\s+)(?P<id1>\d+)",
                  lambda x: x.group("id") + ":" + x.group("id1"), text)
    text = re.sub(r"(?P<id>\d+)(\s+\:|\:\s+|\s+\:\s+)(?P<id1>\d+)",
                  lambda x: x.group("id") + ":" + x.group("id1"), text)

    # chỉnh sửa một số âm , ví dụ òa thành oà
    text = re.sub(r"(?P<id>{})".format("|".join(vn_tone_format.keys())),
                  lambda x: vn_tone_format[x.group("id")], text)

    return text
