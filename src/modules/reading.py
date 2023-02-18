"""NSW dạng số"""
import re
from num2words import num2words

from src.config import *


# Hàm đọc số tự nhiên lớn (>10^9)
def bignumread(number_string: str, index=0) -> str:
    """ index: độ lớn hàng tỷ cần xét """
    if len(number_string) <= 9:
        return smallnumread(number_string)
    else:
        index += 1
        big = number_string[:-9]
        small = number_string[-9:]

        return bignumread(big, index + 1) + " " + "tỷ " * index + " " + smallnumread(small)


# Hàm đọc đọc số tự nhiên nhỏ có chỉnh sửa từ thư viện num2words
def smallnumread(number_string: str) -> str:
    number_value  = int(number_string)
    if number_value <= 1000 or number_value % 100 == 0:
        output_string = num2words(number_value, lang="vi")
    else:
        output_string = num2words(number_value // 100 * 100, lang="vi")
        if (number_value // 100) % 10 == 0:
            output_string += " không trăm"
        if number_value % 100 < 10:
            output_string += " lẻ " + num2words(number_value % 100, lang="vi")
        else:
            output_string += " " + num2words(number_value % 100, lang="vi")
    
    return output_string


# Hàm đọc số tự nhiên
def decimal2words(number_string):
    
    if len(number_string) <= 9:
        return smallnumread(number_string)
    else:
        return bignumread(number_string)


# Hàm đọc NSW dạng số - NUMBER (sỐ thực, số tự nhiên,...) 
def NNUM2words(nnum_string: str) -> str:
    output_string = ""
    if "." in nnum_string and "," in nnum_string:
        nnum_arr = nnum_string.split(",")
        output_string += " phẩy ".join([NNUM2words(nnum_arr[i]) for i in range(len(nnum_arr))])
    elif "," in nnum_string:
        nnum_arr = nnum_string.split(",")
        nnum_arr = nnum_arr[:-1] if nnum_arr[-1] == "00" else nnum_arr
        if len(nnum_arr) == 2:
            output_string = decimal2words(nnum_arr[0]) + " phẩy " + NDIG2words(nnum_arr[1])
        else:
            output_string = decimal2words("".join(nnum_arr))
    elif "." in nnum_string:
        nnum_arr = nnum_string.split(".")
        nnum_arr = nnum_arr[:-1] if nnum_arr[-1] == "00" else nnum_arr
        if len(nnum_arr) == 2:
            if len(nnum_arr[-1]) == 3:
                output_string = decimal2words("".join(nnum_arr))
            else:
                output_string = decimal2words(nnum_arr[0]) + " chấm " + NDIG2words(nnum_arr[1])
        else:
            if nnum_arr[0].startswith("0") or len(nnum_arr[0]) > 3 or any(len(_) != 3 for _ in nnum_arr[1:]):
                output_string = NDIG2words(nnum_arr)
            else:
                output_string = decimal2words("".join(nnum_arr))
    else:
        output_string = decimal2words(nnum_string)

    return "-".join([_ for _ in output_string.split() if _])


# Hàm đọc số dạng phần trăm (VD: 30%, 30-40%)
def NPER2words(nper_string):
    output_string = ""
    nper_string = re.sub(r"\.", ",", nper_string)
    nper_string = re.sub(r"%", " %", nper_string)
    nper_arr = nper_string.split()

    output_string = NNUM2words(nper_arr[0]) + " phần trăm "

    return output_string


# Hàm đọc số thập phân
def NFRC2words(nfrc_string):
    nfrc_arr = nfrc_string.split("/")
    if len(nfrc_arr) == 2:
        output_string = NNUM2words(nfrc_arr[0]) + " phần " + NNUM2words(nfrc_arr[1])
    else:
        output_string = " trên ".join([NNUM2words(nfrc_arr[i]) for i in nfrc_arr])

    return output_string


# Hàm đọc NSW dạng thời gian - TIME
def NTIM2words(time_string):
    output_string = ""
    if "." in time_string:
        time_string = re.sub(r"\.", ",", time_string)
    time_arr = time_string.split(":")
    if time_string.count(":") == 1:
        m = time_arr[0]
        s = time_arr[1]
        if float(s) != 0:
            output_string = NNUM2words(m) + " phút " + NNUM2words(s) + " giây"
        else:
            output_string = NNUM2words(m) + " phút "
    elif time_string.count(":") == 2:
        h = time_arr[0]
        m = time_arr[1]
        s = time_arr[2]
        if time_string.count(",") == 0 and int(s) == 0:
            output_string = NNUM2words(h) + " giờ " + NNUM2words(m) + " phút "
        else:
            output_string = NNUM2words(h) + " giờ " + NNUM2words(m) + " phút " + NNUM2words(s) + " giây"
    elif time_string.count(":") == 0:
        output_string += NNUM2words(time_string)
    else:
        output_string += NNUM2words(time_arr[0])
        for i in range(len(time_arr) - 1):
            output_string += " hai chấm " + NNUM2words(time_arr[i + 1])

    return output_string


# Hàm đọc NSW dạng ngày/tháng - DAY
def NDAY2words(day_string):
    separator = "/"
    day_arr = day_string.split(separator)
    d, m = day_arr[0], day_arr[1]

    # đọc ngày
    if int(m) == 4:
        return NNUM2words(d) + " tháng tư"
    else:
        return NNUM2words(d) + " tháng " + NNUM2words(m)


# Hàm đọc NSW dạng ngày/tháng/năm - DATE
def NDAT2words(date_string):
    separator = "/"
    date_arr = date_string.split(separator)
    d, m, y = date_arr[0], date_arr[1], date_arr[2]

    if int(m) == 4:
        return NNUM2words(d) + " tháng tư năm " + NNUM2words(y)
    else:
        return NNUM2words(d) + " tháng " + NNUM2words(m) + " năm " + NNUM2words(y)


# Hàm đọc NSW dạng tháng/năm - DATE
def NMON2words(mon_string):
    separator = "/"
    mon_arr = mon_string.split(separator)
    m, y = mon_arr[0], mon_arr[1]

    return NNUM2words(m) + " năm " + NNUM2words(y)


# Hàm đọc số dạng kí tự - DIG
def NDIG2words(dig_string):
    output_string = ""
    for i, digit in enumerate(dig_string):
        if i == len(dig_string) - 1 and digit == "5" and i != 0:
            output_string += "lăm"
        elif digit.isdigit():
            output_string += num2words(int(digit), lang="vi") + " "
        elif digit not in  [".", ","]:
            output_string += dict_punc[digit]

    return output_string


def read_currency(cur_word, cur_type):
    if all(_.isdigit() or _ in [".", ","] for _ in cur_word):
        return " ".join([NNUM2words("0" + cur_word if not cur_word[0].isdigit() else cur_word), \
            dict_currency_unit[cur_type]])
    else:
        return " ".join([CSEQ2words(cur_word), \
            dict_currency_unit[cur_type]])


# Hàm đọc đơn vị tiền tệ - CURRENCY
def NCUR2words(ncur_string):
    output_string = ""
    sym_cur = [_ for _ in dict_currency_unit if _ in ncur_string]
    
    if len(sym_cur) == 1:
        ncur_string = ncur_string.replace(sym_cur[0], "").strip()

        return read_currency(ncur_string, sym_cur[0])
    else:
        sym_cur = sorted(sym_cur, key=lambda x: len(x))
        if len(sym_cur) != 0 and all(_ in sym_cur[0] for _ in sym_cur[1:]):
            ncur_string = ncur_string.replace(sym_cur[0], "").strip()
            return read_currency(ncur_string, sym_cur[0])        
        else:
            output_string += CSEQ2words(ncur_string)

    return output_string


# Hàm đọc tuần tự các kí tự
def CSEQ2words(cseq_string: str) -> str:
    output_string = []
    for char in cseq_string:
        if char.upper() in list(dict_vn_chars.keys()):
            output_string.append(dict_vn_chars[char.upper()])
        elif char in list(dict_punc.keys()):
            output_string.append(dict_punc[char])
        elif re.match(r"([0-9])", char):
            output_string.append(num2words(int(char), lang="vi"))

    return " ".join([w for w in output_string if w])


# Hàm đọc ký tự số la mã
roman2int = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000, "IV": 4, "IX": 9, "XL": 40, "XC": 90, "CD": 400, "CM": 900}
def ROMAN2int(number_string: str) -> str:
    i, output_string = 0, 0
    while i < len(number_string):
        if i + 1 < len(number_string) and number_string[i:i + 2] in roman2int:
            output_string += roman2int[number_string[i:i + 2]]
            i += 2
        else:
            output_string += roman2int[number_string[i]]
            i += 1

    return str(output_string)
