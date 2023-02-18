import os
import re
import sys

sys.path.append("models/")
import torch
import pickle
import string
import unidecode
import unicodedata
import numpy as np
from vncorenlp import VnCoreNLP

from .config import *
from .modules.parse import split_compound_nsw, tokenize_nsw
from .modules.utils import *

from .en2vi import dict_en_chars
from .letter2vi import *
from .number2vi import number_normalize


_whitespace_re = re.compile(r'\s+')
class TextNormalizer:
 
    def __init__(self, checkpoint: str, vncorenlp_path: str):
        print("Building Text Nomalizer...")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # load model
        with open(os.path.join(os.path.dirname(checkpoint), "mapping.pkl"), "rb") as f:
            mappings = pickle.load(f)
        self.word_to_idx     = mappings['word_to_id']
        self.char_to_id      = mappings['char_to_id']
        self.idx_to_tag      = {k[1]: k[0].split("-")[-1] for k in mappings['tag_to_id'].items()}

        self.numb_classifier = torch.load(checkpoint).to(self.device)
        self.numb_classifier.eval()

        self.segmenter       = VnCoreNLP(vncorenlp_path, annotators="wseg", max_heap_size='-Xmx500m')

    # Bước 1: Tiền xử lý cho các trường hợp có thể gây tokenize sai
    def token_formatting(self, raw_token: str, prev_token: str, is_start=False) -> str:
        formatted_token = ""
        # Special case for CafeF "============", "*******************",
        if len(raw_token) > 1 and list(set(raw_token)) == 1: 
            formatted_token = ""
        # Skip long token
        elif len(raw_token) > 30 and any(ch not in vn_charsets for ch in raw_token):
            formatted_token = "link đính kèm" \
                if re.match(email_regex, raw_token[:30]) or re.match(url_regex, raw_token[:30]) \
                else ""
            # print(f"\t** \033[92mpre_process condition \033[0m 1     : {raw_token} -> {formatted_token}")
        # phần đọc link/url còn khá khó nên update sau
        elif re.match(email_regex, raw_token) or re.match(url_regex, raw_token):
            formatted_token = URLE2words(raw_token.lower())
            # print(f"\t** \033[92mpre_process condition \033[0m 2     : {raw_token} -> {formatted_token}")
        # Xử lý liệt kê danh sách trong trong document
        elif re.match(r'(\d+.)', raw_token) and (is_start is True and all(_.isdigit() for _ in raw_token[:-1]) and raw_token[-1] == '.'):
            formatted_token = f"{raw_token[:-1]},"
            # print(f"\t** \033[92mpre_process condition \033[0m 3     : {raw_token} -> {formatted_token}")
        # Xứ lý với tên người, tên địa danh,... viết tắt, hoặc từ viết tắt của đơn vị hành chính
        elif "." in raw_token and raw_token.isupper():
            raw_token = [ch for ch in raw_token.split(".") if ch]
            if is_sort(raw_token):
                # Chuẩn hóa tên đơn vị hành chính viết tắt
                if "".join(raw_token) in dict_vn_location and prev_token is not None and prev_token.lower() in dict_vn_location:
                    formatted_token = dict_vn_location["".join(raw_token).lower()].strip()
                else:
                    for ch in raw_token:
                        if ch in dict_vn_chars:
                            formatted_token += f"{dict_vn_chars[ch]} "
                        elif ch in dict_en_chars:
                            formatted_token += f"{dict_en_chars[ch]} "
            # Chuẩn hóa tên đơn vị hành chính viết tắt (dạng: P.2, Q.3,...)
            elif len(raw_token) == 2 and raw_token[0] in dict_vn_location and raw_token[1].isdigit():
                formatted_token = f"{dict_vn_location[raw_token[0]]} {raw_token[1]}"
            else:
                formatted_token = ".".join(raw_token)
            # print(f"\t** \033[92mpre_process condition \033[0m 4     : {raw_token} -> {formatted_token}")
        # Xử lý với tên địa điểm viết tắt
        elif raw_token in dict_double_abb:
            formatted_token = dict_double_abb[raw_token]
            # print(f"\t** \033[92mpre_process condition \033[0m 5     : {raw_token} -> {formatted_token}")       
        # Xử lý trước case bị lỗi khi tách từ: 58:01-58:22, 16:00-24:00
        elif re.match(r"\d+:\d+-\d+:\d+", raw_token):
            if not raw_token[-1].isdigit():
                for i in range(len(raw_token)):
                    if raw_token[len(raw_token) - 1 - i].isdigit():
                        i = len(raw_token) - 1 - i
                        break
                raw_token = raw_token[: i + 1] + " " + raw_token[i + 1:]
            raw_token = raw_token.split()
            formatted_token = " ".join([
                number_normalize(numb_word=raw_token[i],numb_type="TIM") if i == 0 else raw_token[i] \
                    for i in range(len(raw_token))
            ])
        else:
            formatted_token = raw_token

        return formatted_token

    def pre_process(self, in_txts: str) -> str:
        """Loại bỏ các dấu ko cần thiết: gạch ngang | ngoặc đơn | ngoặc kép """
        in_txts = in_txts.replace('–', '-').replace('―', '-').replace('—', '-') \
            .replace('‘', ' ').replace('’', ' ').replace('\'', ' ').replace('´', " ") \
            .replace('“', '"').replace('”', '"').replace('"', ' ')
        in_txts = in_txts.replace("\u200c", "").replace("\u200b", "").replace("\ufeff", "")
        out_txts = [self.token_formatting(token, in_txts[i - 1] if i > 0 else None, True if i == 0 else False) \
            for i, token in enumerate(in_txts.split())]

        return " ".join(out_txts)

    # Bước 2: Tokenize đoạn văn bản, và loại các loại dấu đặc biệt
    def tokenize(self, in_txts: str) -> list :
        """Hàm tách từ sử dụng của VNCoreNLP """
        tkn_txts = []
        for line in self.segmenter.tokenize(in_txts):
            line = " ".join(line).replace("_", " ")
            if any(ch in vn_charsets or ch.isdigit() for ch in line):
                tkn_txts.append(line)
        return tkn_txts

    # Bước 3: Normalize những case đặc biệt, thường hay sai sau quá trình parse các NSW
    def first_normalize(self, in_txts: str) -> str:
        """Hàm chuẩn hóa lần 1 - chủ yếu xử lý với các dạng đặc biệt:
            + Từ được mix giữa chữ và số
            + Các trường hợp khi chuẩn hoá lần lượt ko phát hiện được (hàm normalize lần 2)
            + Xử lý với dấu gây confuse là '/'
        """
        norm_txts = in_txts.split()
        for idx, word in enumerate(norm_txts):
            if is_superscript(word):
                word = "".join([superscript_maps[ch] if ch in superscript_maps else ch for ch in word])                    
                if idx > 0 and word.isdigit() and \
                        all(ch in superscript_maps for ch in norm_txts[idx]) and \
                        any(ch.isdigit() for ch in norm_txts[idx - 1]):
                    norm_txts[idx] = f"mũ {word}"
                else:
                    norm_txts[idx] = word        
            if is_subscript(word):
                word = "".join([subscript_maps[ch] if ch in subscript_maps else ch for ch in word])
                norm_txts[idx] = word

            if word.lower() in list_vn_words:
                continue
            # Xử lý các từ đặc biệt dạng mix chữ/số: s1mple, se7en,...
            elif word.lower() in dict_mix_words:
                norm_txts[idx] = dict_mix_words[word.lower()]
                # print(f"\t** \033[94mfirst_normalize condition \033[0m 1 : {word} -> {norm_txts[idx]}")
            # Xử lý tên celeb, artist Việt Nam
            elif word.lower() in dict_artist:
                norm_txts[idx] = dict_artist[word.lower()]
                # print(f"\t** \033[94mfirst_normalize condition \033[0m 2 : {word} -> {norm_txts[idx]}")
            # Xử lý case bị mix giữa số và chữ
            elif is_complex(word):
                # Tách các số và chữ ra thành từng thành phần
                word = re.sub(r'(?P<id>(\d[{}]))'.format(vn_charsets),
                                lambda x: x.group('id')[0] + ' ' + x.group('id')[1], word)
                word = re.sub(r'(?P<id>([{}]\d))'.format(vn_charsets),
                                lambda x: x.group('id')[0] + ' ' + x.group('id')[1], word)
                word = word.split()                       
                # Xử lý với từ đơn vị dạng: m2, m3,...
                if word[-2] in dict_numb_unit and word[-1] in ["2", "3"]:
                    norm_txts[idx] = " ".join([
                        " ".join(word[: -2]),
                        dict_numb_unit[word[-2]],
                        "vuông" if word[-1] == "2" else "khối"
                    ])
                    # print(f"\t** \033[94mfirst_normalize condition \033[0m 3 : {word} -> {norm_txts[idx]}")
                elif len(word) == 2 and word[1] in dict_numb_unit:
                    norm_txts[idx] = f"{word[0]} {dict_numb_unit[word[1]]}"
                    # print(f"\t** \033[94mfirst_normalize condition \033[0m 4 : {word} -> {norm_txts[idx]}")
                elif len(word) == 3 and word[1] in ["2", "4"]:
                    # Trường hợp tiếng anh viết tắt kiểu iconic M4U, B2B
                    norm_txts[idx] = " ".join([
                        dict_en_chars[word[0]] if word[0] in dict_en_chars else word[0],
                        "two" if word[1] == "2" else "four",
                        dict_en_chars[word[2]] if word[2] in dict_en_chars else word[0]
                    ])
                    # print(f"\t** \033[94mfirst_normalize condition \033[0m 5 : {word} -> {norm_txts[idx]}")
                elif word[0].isdigit() and all(ch in dict_time_unit for i, ch in enumerate(word) if i % 2 == 1):
                    # Xử lý với từ đơn vị thời gian viết tắt: 2h, 2m30s,...
                    norm_txts[idx] = " ".join([dict_time_unit[ch] if ch in dict_time_unit else ch for ch in word])
                    # print(f"\t** \033[94mfirst_normalize condition \033[0m 6 : {word} -> {norm_txts[idx]}")
                else:
                    norm_txts[idx] = " ".join(word)
            # Xử lý case nằm trong dict <dict_double_abb> nhưng bị tách bởi code hoặc BTV
            elif word in ["-", "&", "và"] and 0 < idx < len(norm_txts) - 1:
                ## Note: thông thường những từ đứng 2 bên của từ nối dạng này sẽ là từ viết tắt nếu 
                ## chúng thuộc dạng UPPER
                if "".join(norm_txts[idx - 1: idx + 2]) in dict_double_abb:
                    norm_txts[idx]     = dict_double_abb["".join(norm_txts[idx - 1: idx + 2])]
                    # print(f"\t** \033[94mfirst_normalize condition \033[0m 7 : {' '.join([norm_txts[idx - 1], word, norm_txts[idx + 1]])} -> {norm_txts[idx]}")
                    norm_txts[idx - 1] = norm_txts[idx + 1] = ""
                elif all(txt in dict_mono_abb for txt in [norm_txts[idx - 1], norm_txts[idx + 1]]):
                    norm_txts[idx] = " ".join([
                        dict_mono_abb[norm_txts[idx - 1]],
                        "" if word == "," else "và",
                        dict_mono_abb[norm_txts[idx + 1]]
                    ])
                    # print(f"\t** \033[94mfirst_normalize condition \033[0m 8 : {' '.join([norm_txts[idx - 1], word, norm_txts[idx + 1]])} -> {norm_txts[idx]}")
                    norm_txts[idx - 1] = norm_txts[idx + 1] = ""
                elif re.match(r'([0-9])', norm_txts[idx - 1]) and re.match(r'([0-9])', norm_txts[idx + 1]):
                    norm_txts[idx] = "," if word == "-" else word
            # Xử lý với dấu "/": khá phức tạp (updating)
            elif is_mix_unit(word):
                word = word.split("/")
                if len(word) == 2:
                    norm_txts[idx] = " ".join([
                        dict_numb_unit[word[0]] if word[0] in dict_numb_unit else word[0], 
                        "trên",
                        dict_time_unit[word[1]] if word[1] in dict_time_unit else word[1]
                    ])
                else:
                    norm_txts[idx] = " , ".join(word)
                # print(f"\t** \033[94mfirst_normalize condition \033[0m 9 : {word} -> {norm_txts[idx]}")
            # Xử lý với dấu "/"
            elif "&" in word:
                if len(word) == 3 and word[1] == "&" and word.isupper():
                    word = unidecode.unidecode(word)
                    norm_txts[idx] = f"{dict_en_chars[word[0]]} and {dict_en_chars[word[-1]]}"
                else:
                    norm_txts[idx] = norm_txts[idx].replace("&", " & ")

        return " ".join(norm_txts)

    # Bước 4: Pasrse NSWs
    def parse_nsw(self, in_txts: str) -> str:
        """ Hàm format và compress các NSW thành từng token để dễ chuẩn hoá hơn """
        
        return tokenize_nsw(split_compound_nsw(in_txts))

    # Bước 5: Normalize các NSW còn lại
    def classify_number(self, in_txts: list) -> list:
        word_seqs = torch.LongTensor([self.word_to_idx[w if w in self.word_to_idx else "<UNK>"] for w in in_txts]).to(self.device)
        char_idx  = [[self.char_to_id[ch if ch in self.char_to_id else "<UNK>"] for ch in w] for w in in_txts]
        char_lens = [len(c) for c in char_idx]
        char_seqs = np.zeros((len(char_lens), max(char_lens)), dtype='int')
        for i, c in enumerate(char_idx):
            char_seqs[i, :char_lens[i]] = c
        char_seqs = torch.LongTensor(char_seqs).to(self.device)
        caps_mask = torch.LongTensor([cap_feature(w) for w in in_txts])

        _, labels = self.numb_classifier(word_seqs, char_seqs, caps_mask, char_lens, {})

        return [self.idx_to_tag[l] for l in labels]

    def second_normalize(self, in_txts: list, news_dict: dict, domain: str=None) -> str:
        sequence_tags = self.classify_number(in_txts)
        out_txts = []
        for idx, word in enumerate(in_txts):
            if word == "":
                continue
            # Xử lý dấu (chuyển lên trước cho dễ hướng dẫn)
            elif word in list_punc:
                if word in list_punc_silent:
                    explained_word = "," if idx != len(in_txts) - 1 else "."
                else:
                    explained_word = dict_punc[word] if word in list_punc_read else ""
                out_txts.append(explained_word)           
            # Xử lý với tên ngân hàng (bank)
            elif word.lower() in dict_bank:
                explained_word = dict_bank[word.lower()]
                # print(f"\t** \033[96msecond_normalize condition \033[0m 2: {word} -> {explained_word}")
                out_txts.append(explained_word)
            # Xử lý với từ mượng (loan)
            elif word.lower() in dict_loan_words:
                explained_word = dict_loan_words[word.lower()]
                # print(f"\t** \033[96msecond_normalize condition \033[0m 2: {word} -> {explained_word}")
                out_txts.append(explained_word)
            # Xử lý với tên website
            elif word.lower() in dict_website_name:
                explained_word = dict_website_name[word.lower()]
                # print(f"\t** \033[96msecond_normalize condition \033[0m 2: {word} -> {explained_word}")
                out_txts.append(explained_word)
            # Xử lý với đơn vị tiền tệ
            elif word in dict_currency_unit:
                out_txts.append(dict_currency_unit[word])
            # Xử lý với đơn vị đo só giá trị
            elif word in dict_numb_unit and any(ch.isdigit() for ch in in_txts[idx - 1]):
                explained_word = dict_numb_unit[word]
                out_txts.append(dict_numb_unit[word])
                if idx < len(in_txts) - 1 and in_txts[idx + 1] in ["2", "3"]:
                    out_txts.append("vuông" if in_txts[idx + 1] == "2" else "khối")
                    in_txts[idx + 1] = ""
                # print(f"\t** \033[96msecond_normalize condition \033[0m 4: {word} -> {explained_word}")
            # Xử lý với đơn vị đo thời gian
            elif word in dict_time_unit and any(ch.isdigit() for ch in in_txts[idx - 1]):
                explained_word = dict_time_unit[word]
                out_txts.append(dict_time_unit[word])
                # print(f"\t** \033[96msecond_normalize condition \033[0m 4: {word} -> {explained_word}")
            # Xử lý từ định dạng số (KHÔNG ĐƯỢC THÊM BẤT CỨ RULE NÀO Ở ĐÂY, BẮT BUỘC phải xử lý số trong hàm number_normalize)
            elif any(ch.isdigit() for ch in word):
                if idx == len(in_txts) - 1 and word.endswith("."): word = word[:-1]
                explained_word = number_normalize(
                    numb_word=word,
                    numb_type=sequence_tags[idx]
                )
                # print(f"\t** \033[93mclassify number \033[0m             : {word}({sequence_tags[idx]}) -> {explained_word}")
                out_txts.append(explained_word)
            # Xử lý với từ định dạng UPPER
            elif word.isupper():
                # Xứ kí tự la mã (dạng số)
                if all(ch in ["I", "X", "V"] for ch in word):
                    if len(word) == 1:
                        if (idx > 0) and (in_txts[idx - 1].lower() == 'quý'):
                            explained_word = ROMAN2words(word)
                        else:
                            explained_word = CSEQ2words(word)
                    else:
                        explained_word = ROMAN2words(word)
                    out_txts.append(explained_word)
                # Xử lý từ đơn viết hoa trong tiếng việt
                elif len(word) == 1 and word.lower() in list_vn_words:
                    explained_word = word.lower()
                    out_txts.append(explained_word)
                # Xử lý theo thứ tự ưu tiên: từ điển động | từ điển cố định | đọc từng từ theo tiếng việt
                elif word in news_dict:
                    explained_word = news_dict[word]
                    out_txts.append(explained_word)
                else:
                    # Build từ điển động
                    is_added = False
                    if len(word) < idx < len(in_txts) - 1 and in_txts[idx - 1] == "(" and in_txts[idx + 1] == ")":
                        explained_word = unidecode.unidecode("".join([w[0] for w in in_txts[idx - len(word) - 1: idx - 1]]))
                        if explained_word.upper() == word:
                            news_dict[word] = " ".join(in_txts[idx - len(word) - 1: idx - 1]).lower()
                            is_added = True
                    explained_word = UPPER2words(word, domain) if is_added is False else ""
                    out_txts.append(explained_word)
                # print(f"\t** \033[96msecond_normalize condition \033[0m 3: {word} -> {explained_word}")
            # Xử lý với tù định dạng lower / capitalizer
            elif word.islower() or (word[0].isupper() and word[1:].islower()):
                word = word.lower()
                if word == "x" and 0 < idx < len(in_txts) - 1 and re.match(r'([0-9])', in_txts[idx - 1]) and re.match(r'([0-9])', in_txts[idx + 1]):
                    out_txts.append("nhân")
                elif word in list_vn_words:
                    if idx < len(in_txts) - 1 and word in dict_confuse_words and all(ch in vn_charsets for ch in in_txts[idx + 1]):
                        out_txts.append(LOWER2words(word, domain) if in_txts[idx + 1].lower() not in list_vn_words else word.lower())
                    else:
                        out_txts.append(word.lower())
                elif word in vn_double_consonants.split():
                    out_txts.append(f"{word.lower()}ờ")
                else:
                    out_txts.append(LOWER2words(word, domain))
            # Xử lý case mix
            else:
                spitted_word = re.findall('.[^A-Z]*', unidecode.unidecode(word))
                explained_word = " ".join([dict_en_chars[sub_word] if sub_word.isupper() else LOWER2words(sub_word.lower()) for sub_word in spitted_word])
                # print(f"\t** \033[96msecond_normalize condition \033[0m 5: {word} -> {explained_word}")
                out_txts.append(explained_word)

        return " ".join(out_txts), news_dict

    ## main function ##
    def normalize(self, input_txts: str, domain: str=None, auto_dict: dict={}) -> list:
        # print(f"- raw text      : {input_txts}")
        txts = self.pre_process(unicodedata.normalize('NFC', input_txts))
        # print(f"- pre-processing: {txts}")
        txts = self.tokenize(txts)
        output_txts = [] # audo_dict là từ điển động được xây dựng cho riêng từng bài báo
        for line in txts:
            # print(f"  + sub-text         : {line}")
            line = self.first_normalize(line)
            line = self.parse_nsw(line)
            line, auto_dict = self.second_normalize(line.split(), auto_dict, domain)
            # print(f"  + 2nd normalization: {line}")
            output_txts.append(re.sub(_whitespace_re, " ", line))

        return output_txts, auto_dict
