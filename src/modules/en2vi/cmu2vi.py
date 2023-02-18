import os
import json
import unidecode
import pronouncing
from g2p_en import G2p

cmu2vi_generator = G2p()


############################### CMU2VI DICTIONARY ##################################
cmu2vi_vows          = "AA|AE|AH|AO|AW|AY|EH|ER|EY|IH|IY|OW|OY|UH|UW"
cmu2vi_short_vows    = {"AH": "u", "AA": "o", "IH": "i", "EH": "e", "AE": "a"}
cmu2vi_inshort_vows  = {"u": "AH", "o": "AA", "i": "IH", "e": "EH", "a": "AE"}
cmu2vi_sound_cons    = "B|D|DH|G|JH|L|M|N|NG|R|V|Z|ZH|TR|Q"
cmu2vi_unsound_cons  = "P|T|K|W|F|TH|S|SH|CH|HH"
cmu2vi_cons          = "|".join([cmu2vi_sound_cons, cmu2vi_unsound_cons, "Y"])

cmu2vi_modi_vows     = cmu2vi_vows.split("|")
cmu2vi_modi_vows.extend(["YU", "WA"])
cmu2vi_modi_cons     = cmu2vi_cons.split("|")

latin_mono_vows      = ["/i:/", "/ɑ:/", "/ɔː/", "/u:/", "/ɜː/", "/ʊ/", "/ɪ/", "/e/", "/æ/", "/ʌ/", "/i:ə/"]
latin_duo_vows       = ["/eɪ/", "/əʊ/", "/oʊ/", "/aɪ/", "/ɔɪ/", "/aʊ/", "/ɪə/", "/eə/", "/ʊə/", "/er/", "/ju:/", "/ə/", "/ən/", "/i:əʊ/"]
latin_vows           = latin_mono_vows + latin_duo_vows
latin_sound_cons     = ["/b/", "/d/", "/g/", "/v/", "/δ/", "/z/", "/ʒ/", "/dʒ/", "/m/", "/n/", "/ng/", "/l/","/r/", "/ŋ/", "/w/", "/j/"]
latin_unsound_cons   = ["/p/", "/t/", "/k/", "/kw/", "/f/", "/θ/", "/s/", "/∫/", "/tʃ/", "/h/"]
latin_cons           = latin_sound_cons + latin_unsound_cons

cmu2vi_single_phones = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/en2vi/cmu2vi/mono_phone.json"), "r"))
cmu2vi_double_phones = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/en2vi/cmu2vi/duo_phone.json"), "r"))
cmu2vi_latin         = json.load(open(os.path.join(os.path.dirname(__file__), "dicts/en2vi/cmu2vi/latin.json"), "r"))
####################################################################################
####################################################################################


def special_syllable(en_syllables):
    en_syllables = en_syllables.split()
    for i in range(len(en_syllables)):
        # classify Y syllable
        if en_syllables[i] == "Y":
            if i == 0:
                en_syllables[i] = "Yc"
            elif i == len(en_syllables) - 1:
                en_syllables[i] = "Yv"
            elif en_syllables[i - 1][0] in ["A", "E", "I", "O", "U"] \
                    and en_syllables[i + 1][0] in ["A", "E", "I", "O", "U"]:
                en_syllables[i] = "Yc"
            else:
                en_syllables[i] = "Yv"
        # solve ER case
        if en_syllables[i][:-1] == "ER" and i != len(en_syllables) - 1:
            if en_syllables[i + 1][0] in ["A", "E", "I", "O", "U"]:
                en_syllables[i] += " R"
    en_syllables = " ".join(en_syllables)

    return en_syllables


def normalize_diphthong(en_string, en_syllables):
    output_string = []
    en_syllables = en_syllables.split()
    # find latin vowels
    v_latin = []
    en_string = [_ for _ in en_string]
    for i, en_char in enumerate(en_string):
        if en_char in ["a", "e", "i", "o", "u"]:
            if i == 0:
                v_latin.append(en_char)
            elif i == len(en_string) - 1 and en_char == "e":
                if en_string[i - 1] == "l":
                    v_latin.append("le")
                else:
                    continue
            elif en_string[i - 1] in ["a", "e", "i", "o", "u"]:
                v_latin[-1] += en_char
            else:
                v_latin.append(en_char)

    # combine syllable Y with previous vowel
    for i, en_char in enumerate(en_syllables):
        if en_char == "Yv" and i != 0:
            stress = en_syllables[i - 1][-1]
            if en_syllables[i - 1][0] in ["A", "E", "O", "I"]:
                if en_syllables[i - 1][1] in ["A", "E", "O", "I"]:
                    en_syllables[i - 1] = en_syllables[i - 1][1] + "Y" + stress
                else:
                    en_syllables[i - 1] = en_syllables[i - 1][0] + "Y" + stress
                en_syllables[i] = ""
            elif en_syllables[i - 1][0] in ["U"]:

                en_syllables[i - 1] = "UH" + stress
                en_syllables[i] = ""

    # solve diphthong
    j = 0
    en_syllables = [_ for _ in en_syllables if _]
    for i, en_char in enumerate(en_syllables):
        if not en_char:
            continue
        if j == len(v_latin):
            break
        if en_char[0] in ["A", "E", "U", "I", "O"] or en_char == "Yv":
            if en_char == "Yv" and i != len(en_syllables) - 1:
                if en_syllables[i + 1][0] in ["A", "E", "U", "I", "O"]:
                    if v_latin[j] == "u":
                        en_syllables[i] = "UY" + en_syllables[i + 1][-1]
                        en_syllables[i + 1] = ""
                    else:
                        en_syllables[i] = "IY0"
            if en_char[:-1] == "AA" and v_latin[j] == "o":
                en_syllables[i] = "AO" + en_char[-1]
            j += 1

    en_syllables = [_ for _ in en_syllables if _]
    for i, en_char in enumerate(en_syllables):
        if en_char == "Yv":
            en_syllables[i] = "IY0"
        elif en_char == "Yc":
            en_syllables[i] = "Y"

    en_syllables = [_ for _ in en_syllables if _]

    return " ".join(en_syllables)


def tokenize_syllables(en_syllables):
    en_syllables = en_syllables.split()
    tokenized_syllables = ["_" for _ in en_syllables]

    # find vowel/nuclear
    for i in range(len(en_syllables)):
        if en_syllables[i][0] in ["A", "E", "I", "U", "O"]:
            tokenized_syllables[i] = en_syllables[i][:-1]

    # add consonant/onset
    for i in range(len(en_syllables)):
        if en_syllables[i] in cmu2vi_cons.split("|"):
            # first consonant
            if i == 0:
                if en_syllables[i + 1][0] in ["A", "E", "I", "U", "O"]:
                    tokenized_syllables[i + 1] = en_syllables[i] + " " + tokenized_syllables[i + 1]
            # last consonant
            elif i == len(en_syllables) - 1:
                if en_syllables[i - 1][0] in ["A", "E", "I", "U", "O"]:
                    if en_syllables[i - 1][:-1] not in ["UY", "OY", "ER"]:
                        tokenized_syllables[i - 1] = tokenized_syllables[i - 1] + " " + en_syllables[i]
            # other consonant
            else:
                is_added = False
                if en_syllables[i + 1][0] in ["A", "E", "I", "U", "O"]:
                    tokenized_syllables[i + 1] = en_syllables[i] + " " + tokenized_syllables[i + 1]
                    is_added = True
                if en_syllables[i - 1][0] in ["A", "E", "I", "U", "O"]:
                    # V C V case => V | C V for now
                    if en_syllables[i - 1][:-1] not in ["UY", "OY", "ER"]:
                        if en_syllables[i + 1][0] not in ["A", "E", "I", "U", "O"]:
                            tokenized_syllables[i - 1] = tokenized_syllables[i - 1] + " " + en_syllables[i]
                            is_added = True
                if is_added:
                    tokenized_syllables[i] = ""

    # add single consonant
    for i in range(len(tokenized_syllables)):
        if tokenized_syllables[i] == "_":
            if i == 0:
                if en_syllables[i + 1] == "L":
                    if en_syllables[i] in ["SH", "HH", "Z", "B", "F", "K", "G", "M", "P", "S", "T", "V", "Q", "C"]:
                        tokenized_syllables[i] = en_syllables[i]
                elif en_syllables[i + 1] == "R":
                    if en_syllables[i] in ["SH", "HH", "P", "D", "B", "F", "K", "G", "S", "V", "CH", "TH", "T",
                                           "C"]:
                        tokenized_syllables[i] = en_syllables[i]
                elif en_syllables[i + 1] in ["T", "M", "P", "N", "K", "V"]:
                    if en_syllables[i] in ["S", "SH"]:
                        tokenized_syllables[i] = en_syllables[i]
                elif en_syllables[i + 1] in ["W"]:
                    if en_syllables[i] in ["T", "S", "SH"]:
                        tokenized_syllables[i] = en_syllables[i]
            elif i == len(tokenized_syllables) - 1:
                if en_syllables[i] == "K" and en_syllables[i - 1] == "NG":
                    tokenized_syllables[i] = "K"
            elif 0 < i < len(tokenized_syllables) - 1:
                if en_syllables[i] == "K" and en_syllables[i - 1] == "NG":
                    tokenized_syllables[i] = "K"
                elif en_syllables[i + 1] == "R":
                    if en_syllables[i] in ["G", "D", "T", "P", "K"]:
                        tokenized_syllables[i] = en_syllables[i]
                elif en_syllables[i + 1] == "L":
                    if en_syllables[i] in ["P", "C"]:
                        tokenized_syllables[i] = en_syllables[i]
                elif en_syllables[i + 1] in ["P", "T"]:
                    if en_syllables[i] in ["S"]:
                        tokenized_syllables[i] = en_syllables[i]
            if tokenized_syllables[i] == "_":
                tokenized_syllables[i] = ""

    tokenized_syllables = [_ for _ in tokenized_syllables if _]
    # adding single consonant
    for i in range(len(tokenized_syllables)):
        if i == 0:
            continue
        if tokenized_syllables[i] == "K" and tokenized_syllables[i - 1].endswith("NG"):
            tokenized_syllables[i - 1] += " K"
            tokenized_syllables[i] = ""
    tokenized_syllables = [_ for _ in tokenized_syllables if _]

    # add coda
    if len(tokenized_syllables) > 1 and len(tokenized_syllables[-1].split()) > 2:
        if "IH NG" in tokenized_syllables[-1]:
            if len(tokenized_syllables[-2].split()) < 3 and tokenized_syllables[-2].split()[-1] not in ["UY", "OY"]:
                if tokenized_syllables[-2].split()[-1][0] in ["A", "E", "I", "O", "U"]:
                    tokenized_syllables[-2] += " " + tokenized_syllables[-1].split()[0]

    return tokenized_syllables


def mapping(en_syllables):
    output_string = ""
    en_syllables = en_syllables.split()
    if len(en_syllables) > 4:
        print(f"something wrong in this {' '.join(en_syllables)} syllables!")
    else:
        if len(en_syllables) == 4:
            output_string = cmu2vi_single_phones[en_syllables[0]] + cmu2vi_single_phones[en_syllables[1]] \
                     + cmu2vi_double_phones[" ".join(en_syllables[2:])]
        elif len(en_syllables) == 3:
            output_string = cmu2vi_single_phones[en_syllables[0]] + cmu2vi_double_phones[" ".join(en_syllables[1:])]
        elif len(en_syllables) == 2:
            try:
                output_string = cmu2vi_double_phones[" ".join(en_syllables)]
            except:
                output_string = cmu2vi_single_phones[en_syllables[0]] + cmu2vi_single_phones[en_syllables[1]]
        else:
            if en_syllables[0] in cmu2vi_cons:
                output_string = cmu2vi_single_phones[en_syllables[0]] + "ờ"
            else:
                output_string = cmu2vi_single_phones[en_syllables[0]]

    temp = unidecode.unidecode(output_string)
    if temp.endswith("ing"):
        output_string = output_string[:-1] + "h"
    elif temp.endswith(("enh", "onh", "unh")):
        output_string = output_string[:-1] + "g"

    return output_string


def reading_syllables(en_string, en_syllables):
    output_string = ""
    # Classify Y function => better normalize
    en_syllables = special_syllable(en_syllables)
    en_syllables = normalize_diphthong(en_string, en_syllables)

    if len(en_syllables) < 3:
        output_string += mapping(en_syllables)
    else:
        en_syllables = tokenize_syllables(en_syllables)
        # T R case
        for i in range(len(en_syllables)):
            if i < len(en_syllables) - 1:
                if en_syllables[i][-1] == "T":
                    if en_syllables[i + 1][0] == "R":
                        en_syllables[i + 1] = "T" + en_syllables[i + 1]
                        if len(en_syllables[i]) == 1:
                            en_syllables[i] = ""

        en_syllables = [mapping(en_syllable) for en_syllable in en_syllables if en_syllable]
        output_string += "-".join(en_syllables)

    return output_string


def cmu2vi(en_string: str) -> str:
    en_syllables = pronouncing.phones_for_word(en_string)
    if en_syllables:
        en_syllables = en_syllables[0]
        output_string = reading_syllables(en_string, en_syllables)
    else:
        en_syllables = " ".join(cmu2vi_generator(en_string))
        if en_syllables:
            output_string = reading_syllables(en_string, en_syllables)
        else:
            output_string = ""

    return output_string
