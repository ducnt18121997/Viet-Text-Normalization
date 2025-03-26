import os
import re
import json
import string
from typing import List
from unidecode import unidecode

_whitespace_re = re.compile(r'\s+')


class G2p_vi:
    """ Vietnamese phoneme tokenizer"""

    def __init__(self):
        
        # initialize vietnamese phonemes structure
        self.vowels       = ["a", "e", "i", "o", "u", "y"]
        self.consonants   = {"b": "b", "ch": "ch", "đ": "dd", "ph": "ph", "h": "h", "d": "d", "k": "k", "qu": "kw", "q": "k",
            "c": "k", "l": "l", "m": "m", "n": "n", "nh": "nh", "ng": "ng", "ngh": "ng", "p": "p", "x": "x",
            "s": "s", "t": "t", "th": "th", "tr": "tr", "v": "v", "kh": "kh", "g": "g", "gh": "g", "gi": "d",
            "r": "r"}
        self.medial       = {"u": "wu", "o": "wo"}
        self.monophthongs = {"ă": "aw", "ê": "ee", "e": "e", "â": "aa", "ơ": "ow", "y": "i", "i": "i", "ư": "uw", "ô": "oo",
            "u": "u", "oo": "o", "o": "oa", "a": "a"}
        self.diphthongs   = {"yê": "ie", "iê": "ie", "ya": "ie", "ia": "ie", "ươ": "wa", "ưa": "wa", "uô": "uo", "ua": "uo"}
        self.coda         = {"m": "mz", "n": "nz", "ng": "ngz", "nh": "nhz", "p": "pz", "t": "tz", "ch": "kz", "k": "cz", "c": "cz",
            "u": "uz", "o": "oz", "y": "yz", "i": "iz"}
        self.tone         = {u"á": 1, u"à": 2, u"ả": 3, u"ã": 4, u"ạ": 5,
            u"ấ": 1, u"ầ": 2, u"ẩ": 3, u"ẫ": 4, u"ậ": 5,
            u"ắ": 1, u"ằ": 2, u"ẳ": 3, u"ẵ": 4, u"ặ": 5,
            u"é": 1, u"è": 2, u"ẻ": 3, u"ẽ": 4, u"ẹ": 5,
            u"ế": 1, u"ề": 2, u"ể": 3, u"ễ": 4, u"ệ": 5,
            u"í": 1, u"ì": 2, u"ỉ": 3, u"ĩ": 4, u"ị": 5,
            u"ó": 1, u"ò": 2, u"ỏ": 3, u"õ": 4, u"ọ": 5,
            u"ố": 1, u"ồ": 2, u"ổ": 3, u"ỗ": 4, u"ộ": 5,
            u"ớ": 1, u"ờ": 2, u"ở": 3, u"ỡ": 4, u"ợ": 5,
            u"ú": 1, u"ù": 2, u"ủ": 3, u"ũ": 4, u"ụ": 5,
            u"ứ": 1, u"ừ": 2, u"ử": 3, u"ữ": 4, u"ự": 5,
            u"ý": 1, u"ỳ": 2, u"ỷ": 3, u"ỹ": 4, u"ỵ": 5,
        }
        self.reverse_tone = {u"á": u"a", u"à": u"a", u"ả": u"a", u"ã": u"a", u"ạ": u"a",
            u"ấ": u"â", u"ầ": u"â", u"ẩ": u"â", u"ẫ": u"â", u"ậ": u"â",
            u"ắ": u"ă", u"ằ": u"ă", u"ẳ": u"ă", u"ẵ": u"ă", u"ặ": u"ă",
            u"é": u"e", u"è": u"e", u"ẻ": u"e", u"ẽ": u"e", u"ẹ": u"e",
            u"ế": u"ê", u"ề": u"ê", u"ể": u"ê", u"ễ": u"ê", u"ệ": u"ê",
            u"í": u"i", u"ì": u"i", u"ỉ": u"i", u"ĩ": u"i", u"ị": u"i",
            u"ó": u"o", u"ò": u"o", u"ỏ": u"o", u"õ": u"o", u"ọ": u"o",
            u"ố": u"ô", u"ồ": u"ô", u"ổ": u"ô", u"ỗ": u"ô", u"ộ": u"ô",
            u"ớ": u"ơ", u"ờ": u"ơ", u"ở": u"ơ", u"ỡ": u"ơ", u"ợ": u"ơ",
            u"ú": u"u", u"ù": u"u", u"ủ": u"u", u"ũ": u"u", u"ụ": u"u",
            u"ứ": u"ư", u"ừ": u"ư", u"ử": u"ư", u"ữ": u"ư", u"ự": u"ư",
            u"ý": u"y", u"ỳ": u"y", u"ỷ": u"y", u"ỹ": u"y", u"ỵ": u"y",
        }

        with open(os.path.join(os.path.dirname(__file__), "dicts/words.txt"), "r", encoding="utf8") as f:
            self.vn_words = [x for x in f.read().split("\n") if x]
        self.en_words = {}

    def refix(self, graph: str) -> str:

        if graph.startswith("guo") and len(graph) > 3: graph = f"go{graph[3: ]}"
        if "âu" in graph and not graph.endswith("âu"): graph = graph.replace("âu", "ô")
        if "ây" in graph and not graph.endswith("ây"): graph = graph.replace("ây", "i")
        if "ao" in graph and not graph.endswith("ao"): graph = graph.replace("ao", "o")

        return graph

    def build_phoneme(self, graph: str, _remove_vowel: bool=False) -> List[str]:
        """Tone location: Location of tone in phonemes of word input form: {inside, last, both}
        Two type of phonemes:
        - Tone at end of syllable: C1wVC2T | _consonant, _medial, _vowel, _coda, tone
        - Tone after vowel: C1wVTC2 | _consonant, _medial, f"{_vowel}_{tone}", _coda
        - Tone present both: C1wVTC2T
        """
        
        if _remove_vowel is True and graph.endswith("ờ") and graph[: -1] in self.consonants:
            
            return [self.consonants[graph[:-1]]]
        
        # initilize tone 
        tone = "0"
        graph = list(self.refix(graph))
        for i, w in enumerate(graph):
            if w in self.tone:
                tone = "{}".format(self.tone[w])
                graph[i] = self.reverse_tone[w]
                break

        graph = "".join(graph)
        
        # initilize phonemes
        phone = [graph[0]]
        for i in range(1, len(list(graph))):
            if (unidecode(graph[i]) in self.vowels and unidecode(graph[i - 1]) not in self.vowels) \
                    or (unidecode(graph[i]) not in self.vowels and unidecode(graph[i - 1]) in self.vowels):
                phone.append(" | " + graph[i])
            else:
                phone.append(graph[i])

        phone = [x.strip() for x in "".join(phone).split("|")]
        if unidecode(phone[0][0]) in self.vowels:
            phone = [""] + phone
        phone.extend(["" for _ in range(3 - len(phone))])

        # add consonants
        uni_phone = [unidecode(x) for x in phone]
        # add medial and semi-vowels
        if phone[1]:
            if uni_phone[0] == "g" and uni_phone[1][0] == "i":
                phone[0] = "d"
                phone[1] = phone[1] if uni_phone[1] in ["i", "ieu"] or (phone[1] == "iê" and phone[2]) else phone[1][1:]
            elif uni_phone[0] == "q" and uni_phone[1][0] == "u":
                phone[0] = "qu" if phone[1] != "u" else "c"
                phone[1] = phone[1][1:] if uni_phone[1] != "u" else phone[1]

            if len(phone[1]) > 1:
                if phone[1][-1] in ["u", "o", "i", "y"] and phone[1] not in self.diphthongs and not phone[2]:
                    phone[2] = phone[1][-1]
                    phone[1] = phone[1][:-1]
                if phone[1][0] in ["u", "o"] and phone[1] not in self.diphthongs and phone[1] != "oo":
                    phone[1] = phone[1][0] + " " + phone[1][1:]

        # re-correct consonants
        _consonant = self.consonants[phone[0]] if phone[0] in self.consonants else ""
        if phone[1]:
            phone[1] = phone[1].split()
            # special phonemes o (this must try)
            phone[1][-1] = "oo" if len(phone[1]) == 1 and phone[1][-1] == "o" and phone[2] in ["n", "t", "i"] \
                else phone[1][-1]
            _medial = self.medial[phone[1][0]] if len(phone[1]) == 2 else ""
            _vowel = self.diphthongs[phone[1][-1]] if len(phone[1][-1]) == 2 and phone[1][-1] != "oo"\
                else self.monophthongs[phone[1][-1]]
        else:
            _medial = _vowel = ""

        # add conda
        _coda = self.coda[phone[2]] if phone[2] in self.coda else ""
        _phn  = [_consonant, _medial, f"{_vowel}_{tone}", _coda]

        return [x for x in _phn if x]

    def g2p(self, text: str, foreign_dict: dict=None, get_boundary: bool=True) -> List:
        if foreign_dict is None:
            foreign_dict = self.en_words
        sequences = text.split() if isinstance(text, str) else text

        # initilize phonemes depend on sequence words
        for i, word in enumerate(sequences):
            if foreign_dict is not None and word in foreign_dict:
                if word in self.vn_words:
                    print(word)
                word = foreign_dict[word]["vietlish"]

            # print(f"[*] word(condition 0): {word} => sequences: {sequences[i]}")
            if "-" in word:
                word = word.split("-")
                sequences[i] = [
                    self.build_phoneme(x, _remove_vowel=True if i < len(word) - 1 else False) \
                        for i, x in enumerate(word) if len(x) > 0
                ]
                # if any(x.endswith("ờ") for x in word): 
                #     print(f"[*] word(condition 1): {'-'.join(word)} => sequences: {sequences[i]}")
            else:
                if word in list(string.punctuation):
                    sequences[i] = ["<silent>"]
                else:
                    sequences[i] = self.build_phoneme(word)
        
        # initilize phonemes with boundaries
        expand_sequences, boundaries = [], []
        for seq in sequences:
            if seq is None: continue
            if isinstance(seq[0], list):
                expand_sequences.extend([ph for w in seq for ph in w])
                boundaries.append([len(w) for w in seq])
            else:
                expand_sequences.extend(seq)
                boundaries.append(len(seq))
        
        expand_sequences = [x.upper() for x in expand_sequences]

        if get_boundary is True:
            if expand_sequences[-1] == "<SILENT>": expand_sequences[-1] = "</S>"

            return expand_sequences, boundaries
        else:
            if expand_sequences[-1] != "<SILENT>": expand_sequences.append("<SILENT>")

            return expand_sequences

    def __call__(self, text: str, foreign_dict: dict=None, get_boundary: bool=True):
        # print(text)
        text = re.sub(_whitespace_re, " ", text.lower())

        return self.g2p(text, foreign_dict=foreign_dict, get_boundary=get_boundary)
