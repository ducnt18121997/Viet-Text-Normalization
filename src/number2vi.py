"""
Thư viện đọc NSWs dạng số sang tiếng việt, bao gồm:
- Mô hình phân loại nhãn NSWs (5 dạng: TIM, DAY, MON, NUM, DIG)
- Mô hình phân loại chi tiết dạng NSWs, cụ thể:
    + TIM: NTIM
    + DAY: NDAY, NDAT
    + MON: NMON
    + DIG: NDIG, NTEL, NSCR, NADD, NFRC(24/7, 7/7)
    + NUM: NNUM, NPER, NRNG, NFRC, (CURENCY)
"""
from .modules.reading import *


def TIM2words(tim_string):
    output_string = ""
    if "-" in tim_string:
        tim_arr = tim_string.split("-")
        if "/" in tim_string:
            output_string += " , ".join([
                DAY2words(_string) if "/" in _string else TIM2words(_string)
                for _string in tim_arr
            ])
        else:
            if len(tim_arr) == 2:
                output_string += NTIM2words(tim_arr[0]) + " đến " + NTIM2words(tim_arr[1]) + " "
            else:
                output_string += " ".join([NTIM2words(tim_arr[i]) for i in range(len(tim_arr))])
    elif "/" in tim_string:
        tim_arr = tim_string.split("/")
        if len(tim_arr) == 2:
            if all(len(ch) == 1 for ch in tim_arr):
                output_string += NTIM2words(tim_arr[0]) + " phần " + NTIM2words(tim_arr[1]) + " "
            else:
                output_string += NTIM2words(tim_arr[0]) + " trên " + NTIM2words(tim_arr[1]) + " "
        else:
            output_string += " , ".join(NTIM2words(ch) for ch in tim_string.split("/"))
    else:
        output_string += NTIM2words(tim_string)

    return output_string


def DAY2words(day_string):
    output_string = ""
    if "," in day_string:
        day_arr = day_string.split(",")
        output_string += " ".join([DAY2words(day_arr[i]) for i in range(len(day_arr))])
    elif all(ch in day_string for ch in ["/", ":", "-"]):
        day_arr = day_string.split("-")
        temp_values = []
        for i in range(len(day_arr)):
            if all(ch.isdigit() or ch in ":" for ch in day_arr[i]):
                temp_values.append(TIM2words(day_arr[i]))
            else:
                temp_values.append(DAY2words(day_string[i]))
        output_string += " , ".join(temp_values)
    elif ":" in day_string:
        day_arr = day_string.split(":")
        output_string += DAY2words(day_arr[0]) + " , " + " , ".join([NNUM2words(ch) for ch in day_arr[1:]])
    else:
        if "/" not in day_string:
            # Bắt các trường hợp 25.11-29.11.2020, 18-19.07.2020,...
            if "." in day_string and all(ch.isdigit() for ch in day_string.replace(".","")):
                day_arr = day_string.split(".")
                if len(day_arr) > 3:
                    output_string += NNUM2words(day_string)
                    day_string = ""
                else:
                    if int(day_arr[0]) > 31 or int(day_arr[1]) > 12 or (len(day_arr) == 3 and len(day_arr[2]) > 4):
                        output_string += NNUM2words(day_string)
                        day_string = ""
                    else:
                        day_string = day_string.replace(".", "/")
            # Bắt các trường hợp 2-4-2005, 4-2,...
            elif "-" in day_string and all(ch.isdigit() for ch in day_string.replace("-", "")):
                day_string = day_string.replace("-", "/")
            elif all(ch in day_string for ch in [".", "-"]):
                day_arr = day_string.split("-")
                if len(day_arr) == 2:
                    output_string += DAY2words(day_arr[0]) + " đến " + DAY2words(day_arr[1])
                else:
                    output_string += " , ".join([DAY2words(ch) for ch in day_arr])

                return output_string

        if day_string == "":
            return output_string

        if "-" in day_string:
            day_arr = day_string.split("-")
            for i in range(len(day_arr)):
                # Trường hợp NDAT
                if day_arr[i].count("/") == 2:
                    day_arr[i] = NDAT2words(day_arr[i])
                # Trường hợp NDAY
                elif day_arr[i].count("/") == 1:
                    day_arr[i] = NDAY2words(day_arr[i])
                elif day_arr[i].count("/") == 0:
                    if int(day_arr[i]) < 10:
                        day_arr[i] = "mồng " + NNUM2words(day_arr[i])
                    else:
                        day_arr[i] = NNUM2words(day_arr[i])
                else:
                    day_arr[i] = day_arr.split("/")
                    day_arr[i] = " trên ".join([NNUM2words(day_arr[i][j]) for j in range(len(day_arr[i]))])
            if len(day_arr) == 2:
                output_string += " đến ".join(day_arr) + " "
            else:
                output_string += " , ".join(day_arr) + " "
        else:
            if day_string.count("/") == 2:
                output_string += NDAT2words(day_string)
            elif day_string.count("/") == 1:
                if len(day_string.split("/")[-1]) > 2:
                    output_string += NMON2words(day_string)
                else:
                    output_string += NDAY2words(day_string)
            elif day_string.count("/") == 0:
                output_string += NNUM2words(day_string)
            else:
                day_arr = day_string.split("/")
                output_string += " trên ".join([NNUM2words(day_arr[i]) for i in range(len(day_arr))])

    return output_string


def MON2words(mon_string):
    output_string = ""
    if "," in mon_string:
        mon_arr = mon_string.split(",")
        for i in range(len(mon_arr)):
            output_string += MON2words(mon_arr[i]) + " "
    elif ":" in mon_string:
        mon_arr = mon_string.split(":")
        output_string += MON2words(mon_arr[0]) + " , " + " , ".join([NNUM2words(ch) for ch in mon_arr[1:]])
    else:
        if "/" not in mon_string:
            if "-" in mon_string and "." in mon_string:
                return MON2words(mon_string.replace(".", "/"))
            # Trường hợp dạng: 15-12-1997, 1-6 => 15/12/1997, 1/6 
            elif "-" in mon_string:
                mon_arr = mon_string.split("-")                    
                if mon_string.count("-") == 1:
                    if int(mon_arr[0]) > 12:
                        return NUM2words(mon_string)
                    elif int(mon_arr[-1]) < 12:
                        return NUM2words(mon_string)
                    else:
                        mon_string = mon_string.replace("-", "/")
                else:
                    mon_string = mon_string.replace("-", "/")
            # Trường hợp viết dạng 15.12.1997, 1.6 => 15/12/1997, 1/6
            elif "." in mon_string:
                mon_string = mon_string.replace(".", "/")
        if "-" in mon_string:
            mon_arr = mon_string.split("-")
            for i in range(len(mon_arr)):
                if mon_arr[i].count("/") in [0, 1, 2]:
                    mon_arr[i] = DAY2words(mon_arr[i]) if mon_arr[i].count("/") == 2 else MON2words(mon_arr[i])
                else:
                    mon_arr[i] = mon_arr.split("/")
                    mon_arr[i] = " trên ".join([NNUM2words(mon_arr[i][j]) for j in range(len(mon_arr[i]))])
            if len(mon_arr) == 2:
                output_string += " đến ".join(mon_arr) + " "
            else:
                output_string += " gạch ngang ".join(mon_arr)
        else:
            if mon_string.count("/") == 1:
                try:
                    if int(mon_string.split("/")[-0]) > 12:
                        output_string += NUM2words(mon_string.replace("/", "-"))
                    else:
                        output_string += NMON2words(mon_string)
                except:
                    output_string += NMON2words(mon_string)
            elif mon_string.count("/") == 0:
                output_string += NNUM2words(mon_string)
            else:
                mon_arr = mon_string.split("/")
                output_string += " trên ".join([NNUM2words(mon_arr[i]) for i in range(len(mon_arr))])

    return output_string


def DIG2words(dig_string):
    output_string = ""
    if "/" in dig_string:
        dig_arr = dig_string.split("/")
        output_string += " trên ".join([DIG2words(dig_arr[i]) for i in range(len(dig_arr))])
    elif ":" in dig_string:
        dig_arr = dig_string.split(":")
        output_string += " ".join([DIG2words(dig_arr[i]) for i in range(len(dig_arr))])
    elif "-" in dig_string:
        dig_arr = dig_string.split("-")
        output_string += " ".join([DIG2words(dig_arr[i]) for i in range(len(dig_arr))])
    elif "," in dig_string:
        dig_arr = dig_string.split(",")
        output_string += " phẩy ".join([DIG2words(dig_arr[i]) for i in range(len(dig_arr))])
    elif "." in dig_string:
        dig_arr = dig_string.split(".")
        if len(dig_arr) == 2:
            output_string += " chấm ".join([DIG2words(dig_arr[i]) for i in range(len(dig_arr))])
        else:
            output_string += NDIG2words(dig_string)
    else:
        if all(ch.isdigit() for ch in dig_string):
            output_string += NDIG2words(dig_string)
        else:
            output_string += CSEQ2words(dig_string)

    return output_string


def NUM2words(num_string):
    output_string = ""
    if "-" in num_string:
        num_arr = [x for x in num_string.split("-") if x]
        if len(num_arr) == 2:
            output_string += " đến ".join([NUM2words(num_arr[i]) for i in range(len(num_arr))])
        else:
            output_string += " , ".join([NUM2words(num_arr[i]) for i in range(len(num_arr))])
    elif "/" in num_string:
        num_arr = num_string.split("/")
        if len(num_arr) == 2:
            if all(len(ch) == 1 for ch in num_arr):
                output_string += " phần ".join([NUM2words(num_arr[i]) for i in range(len(num_arr))])
            else:
                output_string += " trên ".join([NUM2words(num_arr[i]) for i in range(len(num_arr))])
        else:
            output_string += " ".join([NUM2words(num_arr[i]) for i in range(len(num_arr))])
    elif ":" in num_string:
        num_arr = num_string.split(":")
        output_string += " , ".join([NUM2words(num_arr[i]) for i in range(len(num_arr))])
    else:
        if "%" in num_string:
            output_string += NPER2words(num_string)
        elif any(ch in num_string for ch in list(dict_currency_unit.keys())):
            output_string = NCUR2words(num_string)
        elif all(ch.isdigit() or ch in [".", ","] for ch in num_string):
            output_string = NNUM2words(num_string) +  " " + output_string
        else:
            output_string = CSEQ2words(num_string) +  " " + output_string

    return output_string


def number_normalize(numb_word: str, numb_type: str) -> str:
    # re-labelling
    prefix, suffix = "", ""
    if "%" in numb_word: 
        numb_type = "NUM"
    if all(ch.isdigit() for ch in numb_word) and numb_word.startswith("0"):
        numb_type = "DIG"
    if numb_word.startswith(("-", "+")) and all(ch.isdigit() or ch in [",", "."] for ch in numb_word[1:]): 
        numb_word = numb_word[1:]
        if numb_type == "NUM": prefix = "trừ" if numb_word[0] == "-" else "cộng"
    if numb_word.endswith("-"):
        numb_word = numb_word[:-1]
        suffix = "đến"
    if numb_word.startswith("-"): 
        numb_word = numb_word[1:]
        prefix = "đến"

    # reading numbers
    if numb_type == "TIM":

        output_string = TIM2words(numb_word)
    elif numb_type == "DAY":

        output_string = DAY2words(numb_word)
    elif numb_type == "MON":

        output_string = MON2words(numb_word)
    elif numb_type == "DIG":

        output_string = DIG2words(numb_word)
    else:

        output_string = NUM2words(numb_word)

    return f"{prefix} {output_string} {suffix}"
