"""
Percent of symbols:
+ two-syllable: 40.7%
+ three-syllable: 92.7%
"""
import os
import json
import warnings

warnings.filterwarnings("ignore")

############################### IPA2VI DICTIONARY ##################################
ipa2vi_mappings      = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/en2vi/ipa2vi/mapping.json")))
ipa2vi_split_oc      = [
    "liquid|nasal", "liquid|stop", "liquid|affricate", "liquid|fricative",
    "stop|nasal", "stop|affricate", "stop|fricative", "stop|aspirate",
    "nasal|liquid", "nasal|stop", "nasal|affricate", "nasal|fricative", "nasal|aspirate",
    "fricative|affricate", "fricative|stop"
]
ipa2vi_double_o      = ["stop", "nasal"]
ipa2vi_conflict_o    = ["V", "DH", "Z", "ZH"]
ipa2vi_connect_c     = ["liquid|stop"]

ipa2vi_mono_phones   = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/en2vi/ipa2vi/mono_phone.json"), "r"))
ipa2vi_duo_phones    = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/en2vi/ipa2vi/duo_phone.json"), "r"))
ipa2vi_pronounces    = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/en2vi/ipa2vi/pronounce.json"), "r"))
ipa2vi_latin         = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/en2vi/ipa2vi/latin.json"), "r"))
####################################################################################
####################################################################################


def ipa2cmu(_ipa: list) -> list:
    _cmu = []
    for ch in _ipa:
        if ch not in ipa2vi_latin:
            print(ch)
            exit()
        _cmu.append(ipa2vi_latin[ch])

    return _cmu


def detect_syllable(_cmu_phone: list, _ipa_phone: list, _type: list):
    # detect vowel
    _syll       = [[_cmu_phone[i]] for i in range(len(_cmu_phone)) if _type[i] == "vowel"]
    _ipa_vowels = [_ipa_phone[i] for i in range(len(_cmu_phone)) if _type[i] == "vowel"]
    _read       = []

    # detect consonant
    vowel_idx, temp = 0, []
    for i in range(len(_cmu_phone)):
        if vowel_idx == len(_syll):
            _syll[vowel_idx - 1] += _cmu_phone[i:]
            break
        if _type[i] == "vowel":
            if len(temp) > 3:
                _syll[vowel_idx] = temp[-3:] + _syll[vowel_idx]
                _syll[vowel_idx - 1] += temp[:-3]
            else:
                _syll[vowel_idx] = temp + _syll[vowel_idx]

            vowel_idx += 1
            temp = []
        else:
            temp.append(_cmu_phone[i])
    # special case
    for i in range(1, len(_syll) - 1):
        if _syll[i - 1][-1] == "ER" and ipa2vi_pronounces[_syll[i][0]] == "vowel":
            _syll[i] = ["R"] + _syll[i]

    # split last coda and first onset
    for i in range(len(_syll)):
        for idx in range(len(_syll[i])):
            if ipa2vi_pronounces[_syll[i][idx]] == "vowel":
                vowel_idx = idx
                break

        onset, nuclear, coda = _syll[i][:vowel_idx], [_syll[i][vowel_idx]], _syll[i][vowel_idx + 1:]
        # onset processing
        if i != 0:
            # process -ly extension
            if i == len(_syll) - 1:
                if len(onset) > 1:
                    if onset[-1] == "L" and nuclear[0] == "IY":
                        _syll[i - 1][-1].extend(onset[:-1])
                        onset = onset[-1:]
            # April McMahon rules
            if len(onset) > 3:
                _syll[i - 1][-1].extend(onset[:-3])
                onset = onset[-3:]
            elif len(onset) == 3 and onset[0] != "S":
                _syll[i - 1][-1].append(onset[0])
                onset = onset[1:]

            if onset:
                if onset[0] in ["NG"]:
                    _syll[i - 1][-1].append(onset[0])
                    onset = onset[1:]

            # coda processing
            if len(onset) == 3:
                if _syll[i - 1][-1] == [""]:
                    _syll[i - 1][-1].append(onset[0])
                    onset = onset[1:]
            elif len(onset) == 2:
                if onset[0] in ipa2vi_conflict_o and onset[1] in ipa2vi_conflict_o:
                    _syll[i - 1][-1].append(onset[0])
                    onset = onset[1:]
                elif onset[0] in ["T", "D", "TH", "B"] and onset[1] == "L":
                    _syll[i - 1][-1].append(onset[0])
                    onset = onset[1:]
                elif ipa2vi_pronounces[onset[0]] == ipa2vi_pronounces[onset[1]] \
                        or "|".join([ipa2vi_pronounces[onset[0]], ipa2vi_pronounces[onset[1]]]) in ipa2vi_split_oc \
                        or onset[0] == "TH":
                    _syll[i - 1][-1].append(onset[0])
                    onset = onset[1:]
                elif onset[0] == "S" and _syll[i - 1][-1] == [""]:
                    _syll[i - 1][-1].append(onset[0])
                    onset = onset[1:]
            elif len(onset) == 1 and _syll[i - 1][-1] == [""]:
                if (ipa2vi_pronounces[onset[0]] in ipa2vi_double_o
                    and _ipa_vowels[i - 1] not in ["ɔː", "aɪ", "ɛ", "ɪ", "iː", "əʊ", "uː", "æ", "ɑː", "ɒ"]
                    and _syll[i - 1][1][0] not in ["ER", "EY"]) \
                        or (_syll[i - 1][1][0] == "EH" and onset[0] in ["SH", "S"] and nuclear[0] == "ER") \
                        or (_syll[i - 1][0][-1] in ["SH", "S"] and _syll[i - 1][1][0] == "ER" and onset[0] in ["N"] and
                            nuclear[0] == "ER"):
                    _syll[i - 1][-1].append(onset[0])

        if len(onset) > 0 and ipa2vi_pronounces[onset[-1]] == "semivowel":
            if onset[-1] == "Y":
                if nuclear[0].startswith("U"):
                    nuclear = ["UY"]
                    onset = onset[:-1]
                else:
                    if len(onset) > 1:
                        nuclear = onset[-1:] + nuclear
                        onset = onset[:-1]
            else:
                if i > 0:
                    _syll[i - 1][-1].extend(onset[:-1])
                    onset = onset[-1:]

        onset = [""] if not onset else onset
        coda = [""] if not coda else coda

        # coda processing
        if "_".join(coda).startswith("NG_K"):
            coda = ["NH"]
        elif "_".join(coda).startswith("S_T"):
            coda = ["T"]
        elif "|".join(coda) == "L|T" and nuclear == ["AO"]:
            nuclear = ["AW"]
            coda = ["SH"]
        elif "|".join([ipa2vi_pronounces[_] for _ in coda if _]).startswith(tuple(ipa2vi_connect_c)) \
                and not "|".join(coda).startswith(("L|D")):
            coda = [coda[1]]
        else:
            for p in coda:
                if p and ipa2vi_pronounces[p] == "nasal":
                    coda = [p]
                    break
        if len(onset) == len(nuclear) == len(coda) == 1:
            if " ".join([nuclear[0], coda[0]]) == "IH NG" and _ipa_vowels[i - 1] not in ["ɔː"]:
                if _syll[i - 1][-1] == [""]:
                    _syll[i - 1][-1] = [onset[0]]

        _syll[i] = [onset, nuclear, coda]

    for i in range(len(_syll)):
        _syll[i] = [[c for c in _ if c] if len(_) > 1 else _ for _ in _syll[i]]
        _onset, _nuclear, _coda = _syll[i]

        if " ".join([_onset[0], _nuclear[0], _coda[0]]) == "W ER K":
            _read.append("guốc")
        elif " ".join([_onset[0], _nuclear[0], _coda[0]]) == "W AH N":
            _read.append("goăn")
        elif " ".join([_onset[0], _nuclear[0], _coda[0]]) == "W IH JH":
            _read.append("guích")
        elif len(_syll) > 1 and len(_onset) == len(_nuclear) == len(_coda) == 1:
            if i == 0:
                if " ".join([_onset[0], _nuclear[0], _coda[0]]) == "K ER N":
                    _read.append("con")
                elif " ".join([_onset[0], _nuclear[0], _coda[0]]).strip() == "ER D":
                    _read.append("át")
                elif " ".join([_onset[0], _nuclear[0], _coda[0]]).strip() == "ER K":
                    _read.append("ác")
                elif " ".join([_onset[0], _nuclear[0], _coda[0]]).strip() == "AE L":
                    _read.append("ôn")
                elif " ".join([_onset[0], _nuclear[0], _coda[0]]).strip() == "AH L":
                    _read.append("ăn")
                elif " ".join([_onset[0], _nuclear[0], _coda[0]]).strip() == "D IH" and _syll[i + 1][0][0] == "F":
                    _read.append("đíp")
                else:
                    _read.append(reading_syllable(_onset, _nuclear, _coda, _ipa_vowels[i]))
            elif i == len(_syll) - 1:
                if " ".join([_onset[0], _nuclear[0], _coda[0]]) == "Z ER M":
                    _read.append("dừm")
                elif " ".join([_onset[0], _nuclear[0], _coda[0]]) == "M EH N":
                    _read.append("mừn")
                elif " ".join([_onset[0], _nuclear[0], _coda[0]]) == "T ER M":
                    _read.append("từm")
                else:
                    _read.append(reading_syllable(_onset, _nuclear, _coda, _ipa_vowels[i]))
            else:
                _read.append(reading_syllable(_onset, _nuclear, _coda, _ipa_vowels[i]))
        else:
            _read.append(reading_syllable(_onset, _nuclear, _coda, _ipa_vowels[i]))
        _syll[i] = ["_".join([c for c in _ if _]) for _ in _syll[i]]

    return [" ".join(_) for _ in _syll], "-".join(_read)


def reading_syllable(_onset, _nuclear, _coda, _ipa_nuclear):
    _nuclear = ["IH", _nuclear[-1]] if len(_nuclear) == 2 else _nuclear

    if _onset:
        _onset = "_".join(_onset)
        if _onset.startswith("K_W") or _onset.startswith("W"):
            if _nuclear[0] == "AO":
                _nuclear[0] = "AE"

        _onset = _onset.replace("T_R", "TR").replace("G_W", "W").replace("K_W", "Q").split("_")

    if _onset:
        _onset = [ipa2vi_mono_phones[_] + "ờ" if i != len(_onset) - 1 else ipa2vi_mono_phones[_] for i, _ in
                  enumerate(_onset) if _]
    else:
        _onset = [""]

    if len(_nuclear) == 2:
        _rhythm = [ipa2vi_mono_phones[_nuclear[0]], ipa2vi_duo_phones[" ".join([_nuclear[1], _coda[0]])]] \
            if " ".join([_nuclear[1], _coda[0]]) in ipa2vi_duo_phones else [ipa2vi_mono_phones[_] for _ in
                                                                               _nuclear]
    else:
        if _ipa_nuclear == "ɜː" and " ".join([_nuclear[0], _coda[0]]) in ["ER L", "ER N"]:
            _rhythm = ["ơn"]
        elif _ipa_nuclear == "ɒ" and " ".join([_nuclear[0], _coda[0]]) in ["AO D", "AO S"]:
            _rhythm = ["ót"]
        elif _ipa_nuclear == "ɑː" and " ".join([_nuclear[0], _coda[0]]) in ["AE K"]:
            _rhythm = ["ác"]
        elif _ipa_nuclear == "ɔː" and " ".join([_nuclear[0], _coda[0]]) in ["AO Z"]:
            _rhythm = ["o"]
        else:
            _rhythm = [ipa2vi_duo_phones[" ".join([_nuclear[0], _coda[0]])]] if " ".join(
                [_nuclear[0], _coda[0]]) in ipa2vi_duo_phones \
                else [ipa2vi_mono_phones[_nuclear[0]]]

    return "-".join(_onset) + "-".join(_rhythm)


def ipa2vi(en_word):
    reading = None
    if en_word in ipa2vi_mappings:
        ipa_ph = ipa2vi_mappings[en_word][0].replace("ˈ", " ").replace("ˌ", " ").split()
        cmu_ph = ipa2cmu(ipa_ph)
        cmu_ph = [ph if not ph[-1].isdigit() else ph[:-1] for ph in cmu_ph]
        cmu_ty = [ipa2vi_pronounces[ph] for ph in cmu_ph]
        _, reading = detect_syllable(cmu_ph, ipa_ph, cmu_ty)

    return reading
