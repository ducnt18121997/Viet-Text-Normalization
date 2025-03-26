import re
import unidecode
import unicodedata
from loguru import logger
from typing import List, Dict
from py_vncorenlp import VnCoreNLP

from .config import *
from .modules.reading import read_nroman
from .modules.utils import *

from .en2vi import dict_en_common_words, dict_en_chars, dict_confuse_words
from .rule import UPPER2words, LOWER2words, NUMBER2words, splitPuncChar, isShortName
from .regrex import display_colors, normalize_by_regrex


class TextNormalizer:
 
    def __init__(self, vncorenlp_path: str, logger: logger=None):
        print("Building Text Nomalizer...")
        self.logger = logger
        self.db_logger = None
        
        self._whitespace_re = re.compile(r"\s+")
        self.rdrsegmenter   = VnCoreNLP(save_dir=vncorenlp_path, annotators=["wseg"])

    # Bước 1: Xử lý các vấn đề liên quan đến encode hoặc các trường hợp gây lỗi khi tokenize bởi VncoreNLP
    def pre_process(self, in_txts: str) -> str:
        out_txts = in_txts.replace('–', '-').replace('―', '-').replace('—', '-') \
            .replace('‘', ' ').replace('’', ' ').replace('\'', ' ').replace('´', " ") \
            .replace('“', '"').replace('”', '"').replace('"', ' ')
        out_txts = out_txts.replace("\u200c", "").replace("\u200b", "").replace("\ufeff", "")\
            .replace("\xa0", " ")
        
        out_txts = out_txts.replace("(", " ( ").replace(")", " ) ")\
            .replace(", ", " , ").replace(" ,", " , ")\
            .replace(". ", " . ").replace(" .", " . ")\
            .replace("*", " * ").replace("=", " = ")\
            .replace("%", " % ").replace("+", " + ")
        
        reg_hotfix = ["km\d\d\+\d+"]
        for _reg in reg_hotfix:
            for match in re.compile(_reg).finditer(out_txts):
                _tmp = match.group()
                mtxt = _tmp.replace("+", " + ")
                out_txts = out_txts.replace(match.group(), mtxt)

        return re.sub(self._whitespace_re, " ", out_txts).strip()

    # Bước 2: Chuẩn hóa bằng regrex và tokenize văn bản bằng vncorenlp
    def tokenize(self, in_txts: str) -> List[str]:
        out_txts = normalize_by_regrex(in_txts)
        out_txts = self.rdrsegmenter.word_segment(out_txts)

        return out_txts

    # Bước 3: Chuẩn hóa văn bản bằng luật
    def normalize(self, in_txts: List, news_dict: Dict=[]) -> str:
        if isinstance(in_txts, str): in_txts = in_txts.split()
        out_txts = []
        print(in_txts)
        for idx, word in enumerate(in_txts):
            if word is None: continue
            if is_superscript(word):
                word = "".join([superscript_maps[ch] if ch in superscript_maps else ch for ch in word])
            if is_subscript(word):
                word = "".join([subscript_maps[ch] if ch in subscript_maps else ch for ch in word])
            
            # Xử lý dấu (chuyển lên trước cho dễ hướng dẫn)
            if word in list_punc or all(x in string.punctuation for x in word):
                if idx == 0:
                    explained_word = ""
                elif len(word) > 1:
                    explained_word = ","
                elif word in list_punc_silent:
                    explained_word = "," if idx != len(in_txts) - 1 else "."
                else:
                    explained_word = dict_punc[word] if word in list_punc_read else ""
                out_txts.append(explained_word)    
            elif word.lower() in dict_spec_words:
                explained_word = dict_spec_words[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (spec word) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            # Xử lý với các từ điển artist/bank/loan/mix/symbol/website/currency
            elif word.lower() in dict_artist:
                explained_word = dict_artist[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (artist) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in dict_bank:
                explained_word = dict_bank[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (bank) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in dict_loan_words:
                explained_word = dict_loan_words[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (loan) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in dict_mix_words:
                explained_word = self.normalize(dict_mix_words[word.lower()])[0]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (mix) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif any(ch in word for ch in dict_symbol):
                for ch in dict_symbol: 
                    if ch in word: spitted_word = word.replace(ch, f" {ch} ")
                explained_word = " ".join([self.normalize(_word)[0] if _word not in dict_symbol else dict_symbol[_word] for _word in spitted_word])
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (symbol) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in dict_website_name:
                explained_word = dict_website_name[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (website) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in dict_website_domain:
                explained_word = dict_website_domain[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (website) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.endswith(list_website_domain):
                explained_word = self.normalize(word.replace(".", " chấm "))[0]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (website) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word in dict_currency_unit:
                explained_word = dict_currency_unit[word]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (currency) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif isShortName(word):
                explained_word = UPPER2words(word)
                out_txts.append(explained_word)
            elif word.startswith(list_vn_location):
                spitted_word   = [w for w in word.split(".") if w]
                explained_word = [dict_vn_location[spitted_word[0]]]
                if len(spitted_word) != 1:
                    explained_word.append(self.normalize(".".join(spitted_word)[1: ])[0])
                explained_word = " ".join(explained_word)
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (đia điểm) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif any(ch.isdigit() for ch in word):
                explained_word = NUMBER2words(word)
                out_txts.append(explained_word)
            # Xử lý case missmatch sau khi tokenize
            elif word.endswith("."):
                explained_word = f"{self.normalize(word[: -1])[0]} ."
                # print(f"\t** {display_colors.YELLOW} đọc định dạng số còn sót {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif "-" in word:
                if word.isupper():
                # Xử lý từ viết tắt theo cặp [cặp 2 | cặp 3]
                    _word = word.replace("-", "#")
                    if _word in dict_duo_abb:
                        explained_word = dict_duo_abb[_word]
                    else:
                        explained_word = self.normalize(_word.replace("#", " "))[0]
                else:
                    explained_word = " ".join(self.normalize(_word)[0] for _word in word.split("-"))
                # print(f"\t** {display_colors.YELLOW} đọc định dạng số còn sót {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif "/" in word:
                if word in dict_base_unit:
                    explained_word = dict_base_unit[word]
                else:
                    explained_word = self.normalize(word.replace("/", " / "))[0]
                out_txts.append(explained_word)
            # Xử lý với từ định dạng [UPPER]
            elif word.isupper():
                # Xử lý từ đơn viết hoa trong tiếng việt
                if all(ch in "IVX" for ch in word):
                    if len(word) == 1:
                        explained_word = UPPER2words(word)
                    else:
                        explained_word = read_nroman(word)
                # Xử lý các kí tự tiếng việt đọc được nhưng viết hoa
                elif len(word) == 1 and word.lower() in list_vn_words:
                    explained_word = word.lower()
                elif word in list_start_duo_abb:
                    if idx < len(in_txts) - 5 and f"{word}#{in_txts[idx + 2]}#{in_txts[idx + 4]}" in dict_duo_abb:
                        explained_word = dict_duo_abb[f"{word}#{in_txts[idx + 2]}#{in_txts[idx + 4]}"]
                        for i in range(4): in_txts[idx + 1 + i] = None
                    elif idx < len(in_txts) - 3 and f"{word}#{in_txts[idx + 2]}" in dict_duo_abb:
                        explained_word = dict_duo_abb[f"{word}#{in_txts[idx + 2]}"]
                        for i in range(2): in_txts[idx + 1 + i] = None
                    else: 
                        explained_word = UPPER2words(word)
                # Xử lý theo thứ tự ưu tiên: từ điển động | từ điển cố định | đọc từng từ theo tiếng việt
                elif word in news_dict:
                    explained_word = news_dict[word]
                else:
                    # Build từ điển động
                    is_added = False
                    if len(word) < idx < len(in_txts) - 1 and in_txts[idx - 1] == "(" and in_txts[idx + 1] == ")" and all(w is not None for w in in_txts[idx - len(word) - 1: idx - 1]):
                        explained_word = unidecode.unidecode("".join([w[0] for w in in_txts[idx - len(word) - 1: idx - 1]]))
                        if explained_word.upper() == word and all(w.lower() in list_vn_words for w in in_txts[idx - len(word) - 1: idx - 1]):
                            news_dict[word] = " ".join(in_txts[idx - len(word) - 1: idx - 1]).lower()
                            is_added = True
                    explained_word = UPPER2words(word) if is_added is False else ""
                    try:
                        if self.logger is not None:
                            if self.db_logger is not None :
                                if word not in self.db_logger:
                                    self.db_logger[word] = {"read": explained_word.replace(" ", "_"), "count": 1}
                                    self.logger.info(f"\t {word} -> {explained_word.replace(' ', '_')}")
                                else:
                                    self.db_logger[word]["read"]  = explained_word.replace(" ", "_")
                                    self.db_logger[word]["count"] += 1
                    except:
                        pass
                # if explained_word != word.lower():
                    # print(f"\t** {display_colors.YELLOW} đọc định dạng viết hoa {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            # Xử lý với tù định dạng [lower] / [Capitalizer]
            elif word.islower() or (word[0].isupper() and word[1:].islower()):
                word = word.lower()
                if word == "x" and 0 < idx < len(in_txts) - 1 and re.match(r'([0-9])', in_txts[idx - 1]) and re.match(r'([0-9])', in_txts[idx + 1]):
                    explained_word = "nhân"
                elif word in list_vn_words:
                    if word in dict_confuse_words:
                        if idx < len(in_txts) - 1:
                            if in_txts[idx + 1].lower() in dict_vn_words or len(in_txts[idx + 1]) == 1:
                                explained_word = word.lower()
                            elif in_txts[idx + 1][0].isdigit():
                                explained_word = word.lower()
                            elif in_txts[idx + 1] in string.punctuation:
                                explained_word = word.lower()
                            else:
                                explained_word = dict_confuse_words[word]
                        else:
                            explained_word = word
                    else:
                        explained_word = word.lower()
                elif word in vn_double_consonants.split():
                    explained_word = f"{word.lower()}ờ"
                else:
                    explained_word = LOWER2words(word)
                # if explained_word != word.lower():
                #     print(f"\t** {display_colors.DARKCYAN} đọc định dạng viết thường (tiếng anh,...) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            # Xử lý case mix toàn chữ
            elif all(ch in vn_charsets for ch in word):
                spitted_word   = "".join(_word if _word.isupper() else f" {_word} " for _word in re.findall('.[^A-Z]*', word))
                explained_word = []
                for i, _word in enumerate(spitted_word.split()):
                    if i == 0 and _word == "i":
                        explained_word.append("ai")
                    elif _word.isupper():
                        if _word in dict_mono_abb:
                            explained_word.append(dict_mono_abb[_word])
                        elif _word.lower() in dict_en_common_words:
                            explained_word.append(dict_en_common_words[_word.lower()])
                        elif any(ch not in dict_en_chars for ch in _word):
                            explained_word.append(LOWER2words(_word.lower()))
                        else:
                            explained_word.append(" ".join([dict_en_chars[ch] for ch in _word]))
                    else:
                        explained_word.append(_word.lower() if _word.lower() in dict_vn_words else LOWER2words(_word.lower()))
                explained_word = " ".join(explained_word)
                out_txts.append(explained_word)
            # Xử lý case còn lại
            else:
                spitted_word = splitPuncChar(word).replace("-", " ")
                if word.endswith(tuple([f".{k}" for k in dict_website_domain.keys()])):
                    spitted_word = spitted_word.replace(".", "chấm")
                explained_word = []
                for _word in spitted_word.split():
                    if _word.lower() in list_vn_words:
                        explained_word.append(_word.lower())
                    elif _word in string.punctuation:
                        if all(w in list_vn_words or w in string.punctuation for w in spitted_word.split()):
                            explained_word.append(",")
                    else:
                        explained_word.append(UPPER2words(_word) if _word.isupper() else LOWER2words(_word.lower()))
                explained_word = " ".join(explained_word)
                # print(f"\t** {display_colors.PURPLE} đọc định dạng viết mix có dấu câu {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
        out_txts = " ".join(out_txts)

        return re.sub(self._whitespace_re, " ", out_txts).strip(), news_dict

    def __call__(self, itexts: str, auto_dict: Dict={}) -> List:
        _texts = self.pre_process(unicodedata.normalize('NFC', itexts)).split("\n")
        otexts = [] # audo_dict là từ điển động được xây dựng cho riêng từng bài báo
        for line in _texts:
            if not line: continue
            line = self.tokenize(line)
            for _sent in line:
                print(_sent)
                # NOTE(by ducnt2): Hot-fix cho tokenizer
                _sent = _sent.replace("T T&T T", "TT&TT")
                _sent, auto_dict = self.normalize(_sent.replace("_", " "), auto_dict)
                otexts.append(_sent)

        return otexts, auto_dict
