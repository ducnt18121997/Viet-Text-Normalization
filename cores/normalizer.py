import os
import re
import string
import unicodedata
import constants
from loguru import logger
from typing import List, Dict
from py_vncorenlp import VnCoreNLP
from cores import reader, regrex
from utils.helper import is_short_name, split_punc_char


logger.add(
    "logs/normalizer.log",
    level="INFO",
    format="{time} {level} {message}",
    rotation="10 MB",
    compression="zip",
)


class TextNormalizer:

    def __init__(self, vncorenlp_path: str):
        print("Building Text Nomalizer...")
        self.logger = logger
        self.db_logger = None

        self._whitespace_re = re.compile(r"\s+")
        vncorenlp_path = os.path.abspath(vncorenlp_path)
        if not os.path.exists(vncorenlp_path):
            from py_vncorenlp import download_model

            os.makedirs(vncorenlp_path, exist_ok=True)
            download_model(save_dir=os.path.abspath(vncorenlp_path))

        self.rdrsegmenter = VnCoreNLP(save_dir=vncorenlp_path, annotators=["wseg"])

    # Bước 1: Xử lý các vấn đề liên quan đến encode hoặc các trường hợp gây lỗi khi tokenize bởi VncoreNLP
    def pre_process(self, in_txts: str) -> str:
        out_txts = (
            in_txts.replace("–", "-")
            .replace("―", "-")
            .replace("—", "-")
            .replace("‘", " ")
            .replace("’", " ")
            .replace("'", " ")
            .replace("´", " ")
            .replace("“", '"')
            .replace("”", '"')
            .replace('"', " ")
        )
        out_txts = (
            out_txts.replace("\u200c", "")
            .replace("\u200b", "")
            .replace("\ufeff", "")
            .replace("\xa0", " ")
        )

        out_txts = (
            out_txts.replace("(", " ( ")
            .replace(")", " ) ")
            .replace(", ", " , ")
            .replace(" ,", " , ")
            .replace(". ", " . ")
            .replace(" .", " . ")
            .replace("*", " * ")
            .replace("=", " = ")
            .replace("%", " % ")
            .replace("+", " + ")
        )

        return regrex.RegrexNormalize.whitespace(out_txts)

    # Bước 2: Chuẩn hóa bằng regrex và tokenize văn bản bằng vncorenlp
    def tokenize(self, in_txts: str) -> List[str]:
        out_txts = regrex.normalize(in_txts)
        out_txts = self.rdrsegmenter.word_segment(out_txts)

        return out_txts

    # Bước 3: Chuẩn hóa văn bản bằng luật
    def normalize(self, in_txts: List) -> str:
        if isinstance(in_txts, str):
            in_txts = in_txts.split()

        out_txts = []
        for idx, word in enumerate(in_txts):
            if word is None:
                continue

            # Xử lý dấu (chuyển lên trước cho dễ hướng dẫn)
            if word in constants.PunctuationCharset.PUNCTUATION or all(
                x in string.punctuation for x in word
            ):
                if idx == 0:
                    explained_word = ""
                elif len(word) > 1:
                    explained_word = ","
                elif word in constants.PunctuationCharset.SILENT:
                    explained_word = "," if idx != len(in_txts) - 1 else "."
                else:
                    explained_word = (
                        constants.PunctuationCharset.READER[word]
                        if word in constants.PunctuationCharset.PUNCTUATION
                        else ""
                    )
                out_txts.append(explained_word)
            elif word.lower() in constants.VietnameseWord.WORDS:
                explained_word = word.lower()
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (spec word) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            # Xử lý với các từ điển artist/bank/loan/mix/symbol/website/currency
            elif word.lower() in constants.VietnameseArtist.ARTIST:
                explained_word = constants.VietnameseArtist.READER[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (artist) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in constants.VietnameseBank.BANK:
                explained_word = constants.VietnameseBank.BANK[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (bank) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in constants.VietnameseLoanWord.LOAN_WORD:
                explained_word = constants.VietnameseLoanWord.LOAN_WORD[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (loan) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in constants.VietnameseMixWord.MIX_WORD:
                explained_word = self.normalize(
                    constants.VietnameseMixWord.MIX_WORD[word.lower()]
                )[0]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (mix) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif any(ch in word for ch in constants.SymbolCharset.SYMBOL):
                for ch in constants.SymbolCharset.SYMBOL:
                    if ch in word:
                        spitted_word = word.replace(ch, f" {ch} ")
                explained_word = " ".join(
                    [
                        (
                            self.normalize(_word)[0]
                            if _word not in constants.SymbolCharset.SYMBOL
                            else constants.SymbolCharset.READER[_word]
                        )
                        for _word in spitted_word
                    ]
                )
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (symbol) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in constants.VietnameseWebsite.WEBSITE:
                explained_word = constants.VietnameseWebsite.READER[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (website) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.lower() in constants.VietnameseWebsite.DOMAIN:
                explained_word = constants.VietnameseWebsite.READER[word.lower()]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (website) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word.endswith(tuple(constants.VietnameseWebsite.DOMAIN)):
                explained_word = self.normalize(word.replace(".", " chấm "))[0]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (website) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif word in constants.CurrencyCharset.CURRENCY:
                explained_word = constants.CurrencyCharset.READER[word]
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (currency) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif is_short_name(word):
                explained_word = reader.WordReader.upper(word)
                out_txts.append(explained_word)
            elif word.startswith(tuple(constants.VietnameseLocation.LOCATION)):
                spitted_word = [w for w in word.split(".") if w]
                explained_word = [constants.VietnameseLocation.READER[spitted_word[0]]]
                if len(spitted_word) != 1:
                    explained_word.append(self.normalize(".".join(spitted_word)[1:])[0])
                explained_word = " ".join(explained_word)
                # print(f"\t** {display_colors.PURPLE} đọc từ điển cố định (đia điểm) {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif any(ch.isdigit() for ch in word):
                explained_word = reader.NumberReader.number(word)
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
                    if _word in constants.VietnameseAbbreviation.DOUBLE_ABBREVIATION:
                        explained_word = (
                            constants.VietnameseAbbreviation.DOUBLE_ABBREVIATION[_word]
                        )
                    else:
                        explained_word = self.normalize(_word.replace("#", " "))[0]
                else:
                    explained_word = " ".join(
                        self.normalize(_word)[0] for _word in word.split("-")
                    )
                # print(f"\t** {display_colors.YELLOW} đọc định dạng số còn sót {display_colors.ENDC}: {word} -> {explained_word}")
                out_txts.append(explained_word)
            elif "/" in word:
                if word in constants.UnitCharset.UNIT:
                    explained_word = constants.UnitCharset.READER[word]
                else:
                    explained_word = self.normalize(word.replace("/", " / "))[0]
                out_txts.append(explained_word)
            # Xử lý với từ định dạng [UPPER]
            elif word.isupper():
                # Xử lý từ đơn viết hoa trong tiếng việt
                if all(ch in "IVX" for ch in word):
                    if len(word) == 1:
                        explained_word = reader.WordReader.upper(word)
                    else:
                        explained_word = reader.NumberReader.roman(word)
                # Xử lý các kí tự tiếng việt đọc được nhưng viết hoa
                elif len(word) == 1 and word.lower() in constants.VietnameseWord.WORDS:
                    explained_word = word.lower()
                elif word in constants.VietnameseAbbreviation.START_DOUBLE_ABBREVIATION:
                    if (
                        idx < len(in_txts) - 5
                        and f"{word}#{in_txts[idx + 2]}#{in_txts[idx + 4]}"
                        in constants.VietnameseAbbreviation.DOUBLE_ABBREVIATION
                    ):
                        explained_word = (
                            constants.VietnameseAbbreviation.DOUBLE_ABBREVIATION[
                                f"{word}#{in_txts[idx + 2]}#{in_txts[idx + 4]}"
                            ]
                        )
                        for i in range(4):
                            in_txts[idx + 1 + i] = None
                    elif (
                        idx < len(in_txts) - 3
                        and f"{word}#{in_txts[idx + 2]}"
                        in constants.VietnameseAbbreviation.DOUBLE_ABBREVIATION
                    ):
                        explained_word = (
                            constants.VietnameseAbbreviation.DOUBLE_ABBREVIATION[
                                f"{word}#{in_txts[idx + 2]}"
                            ]
                        )
                        for i in range(2):
                            in_txts[idx + 1 + i] = None
                    else:
                        explained_word = reader.WordReader.upper(word)
                else:
                    explained_word = reader.WordReader.upper(word)
                out_txts.append(explained_word)
            # Xử lý với tù định dạng [lower] / [Capitalizer]
            elif word.islower() or (word[0].isupper() and word[1:].islower()):
                word = word.lower()
                if (
                    word == "x"
                    and 0 < idx < len(in_txts) - 1
                    and re.match(r"([0-9])", in_txts[idx - 1])
                    and re.match(r"([0-9])", in_txts[idx + 1])
                ):
                    explained_word = "nhân"
                elif word in constants.VietnameseCharset.DOUBLE_CONSONANTS.split():
                    explained_word = f"{word.lower()}ờ"
                else:
                    explained_word = reader.WordReader.lower(word)
                out_txts.append(explained_word)
            # Xử lý case mix toàn chữ
            elif all(ch in constants.VietnameseCharset.CHARSETS for ch in word):
                explained_word = "".join(
                    _word if _word.isupper() else f" {_word} "
                    for _word in re.findall(".[^A-Z]*", word)
                )
                out_txts.append(explained_word)
            # Xử lý case còn lại
            else:
                spitted_word = split_punc_char(word).replace("-", " ")
                if word.endswith(
                    tuple([f".{k}" for k in constants.VietnameseWebsite.DOMAIN.keys()])
                ):
                    spitted_word = spitted_word.replace(".", "chấm")
                explained_word = []
                for _word in spitted_word.split():
                    if _word.lower() in list_vn_words:
                        explained_word.append(_word.lower())
                    elif _word in string.punctuation:
                        if all(
                            w in constants.VietnameseWord.WORDS
                            or w in string.punctuation
                            for w in spitted_word.split()
                        ):
                            explained_word.append(",")
                    else:
                        explained_word.append(
                            reader.WordReader.upper(_word)
                            if _word.isupper()
                            else reader.WordReader.lower(_word.lower())
                        )
                explained_word = " ".join(explained_word)
                out_txts.append(explained_word)
        out_txts = " ".join(out_txts)

        return re.sub(self._whitespace_re, " ", out_txts).strip()

    def __call__(self, itexts: str) -> List[str]:
        otexts = []
        for line in self.pre_process(unicodedata.normalize("NFC", itexts)).split("\n"):
            if not line:
                continue
            line = self.tokenize(line)
            for sentence in line:
                sentence = sentence.replace("T T&T T", "TT&TT")
                sentence = self.normalize(sentence.replace("_", " "))
                otexts.append(sentence)

        return otexts
