import unicodedata
from num2words import num2words


# func hỗ trợ đọc số
def bignumread(istring: str, index=0) -> str:
    """ index: độ lớn hàng tỷ cần xét """
    if len(istring) <= 9:
        return smallnumread(istring)
    else:
        index += 1
        big   = istring[:-9]
        small = istring[-9:]
        return bignumread(big, index + 1) + " " + "tỷ " * index + " " + smallnumread(small)


def smallnumread(istring: str) -> str:
    number_value  = int(istring)
    if number_value <= 1000 or number_value % 100 == 0:
        ostring = num2words(number_value, lang="vi")
    else:
        ostring = num2words(number_value // 100 * 100, lang="vi")
        if (number_value // 100) % 10 == 0:
            ostring += " không trăm"
        if number_value % 100 < 10:
            ostring += " lẻ " + num2words(number_value % 100, lang="vi")
        else:
            ostring += " " + num2words(number_value % 100, lang="vi")
    
    return ostring


def decimal2words(istring: str) -> str:
    istring = unicodedata.normalize("NFKC", istring.strip())
    if len(istring) <= 9:
        return smallnumread(istring)
    else:
        return bignumread(istring)


def get_separator(string: str) -> str:
    if "/" in string: separator = "/"
    elif "-" in string: separator = "-"
    elif "." in string: separator = "."
    else: raise TypeError(f"Unidentify separator, given string: {string}")

    return separator


# nsw dạng ngày/tháng/năm
def read_ndate(istring: str) -> str:
    separator = get_separator(istring)
    d, m, y   = [v for v in istring.split(separator)]
    ostring   = f" {smallnumread(d)} tháng tư năm {smallnumread(y)} " if int(m) == 4 else \
        f" {smallnumread(d)} tháng {smallnumread(m)} năm {smallnumread(y)} "

    return ostring


def read_nday(istring: str) -> str:
    if all(c.isdigit() for c in istring): 
        return smallnumread(istring)
    
    separator = get_separator(istring)
    if istring.count(separator) == 2: 
        return read_ndate(istring)
    
    d, m    = [v for v in istring.split(separator)]
    ostring =  f" {smallnumread(d)} tháng tư " if int(m) == 4 else \
        f" {smallnumread(d)} tháng {smallnumread(m)} "

    return ostring


def read_nmon(istring: str, is_quarter: bool=False) -> str:
    if all(c.isdigit() for c in istring): 
        return smallnumread(istring)
    if all(not c.isdigit() for c in istring):
        return read_nroman(istring)

    separator = get_separator(istring)
    m, y      = istring.split(separator)
    ostring   = f" {read_nroman(m) if is_quarter is True else smallnumread(m)} năm {smallnumread(y)} " 

    return ostring


# Hàm đọc NSW dạng thời gian
def read_ntime(istring: str) -> str:
    # type 1: xx:xx:xx
    if ":" in istring:
        _string = istring.split(":")
        if len(_string) == 2:
            h, m    = _string
            ostring = f" {smallnumread(h)} giờ "
            if int(m.strip()) != 0: ostring += f" {smallnumread(m)} phút "
        elif len(_string) == 3:
            h, m, s = _string
            ostring = f" {smallnumread(h)} giờ {smallnumread(m)} phút "
            if int(s.strip()) != 0: ostring += f" {smallnumread(s)} giây"
        else:
            raise NotImplementedError
    # type 2: xx{h}xx{m}xx{s}
    else:
        tstring = istring.lower()
        tstring = tstring.replace("h", " giờ ")
        tstring = tstring.replace("m", " phút ")
        tstring = tstring.replace("s", " giây ")
        tstring = tstring.split()
        if len(tstring) % 2 == 0:
            ostring = [x if not x.isdigit() else smallnumread(x) for i, x in enumerate(tstring)]
        else:
            ostring = [x if not x.isdigit() else smallnumread(x) for i, x in enumerate(tstring[: -1])]
            if int(tstring[-1]) != 0 or len(tstring) == 1: ostring.append(smallnumread(tstring[-1]))
        ostring = " ".join(ostring)

    return ostring


def read_nnumber(istring: str, is_decimal: bool=True) -> str:
    ostring = ""
    if istring.startswith("-"):
        ostring += " âm "
        istring = istring[1: ]
    elif "+" in istring or "-" in istring:
        _string = istring.replace("-", " trừ ").replace("+", " cộng ").split()
        ostring = " ".join([read_nnumber(x) if x not in ["cộng", "trừ"] else x for x in _string])
    elif "." in istring and "," in istring:
        nnum_arr = istring.split(",")
        ostring += " phẩy ".join([read_nnumber(nnum_arr[i], is_decimal=False) for i in range(len(nnum_arr))])
    elif "," in istring:
        if is_decimal is True and istring.count(",") == 1 and not istring.endswith("00"):
            num, fra = istring.split(",")
            ostring += f" {decimal2words(num)} phẩy {decimal2words(fra) if len(fra) < 3 else read_ndigit(fra)}"
        else:
            ostring += decimal2words(istring.replace(",", ""))
    elif "." in istring:
        istring = istring.replace(".", ",")
        if is_decimal is True and istring.count(",") == 1 and len(istring.split(",")[-1]) != 3:
            num, fra = istring.split(",")
            ostring += f" {decimal2words(num)} phẩy {decimal2words(fra) if len(fra) < 3 else read_ndigit(fra)}"
        else:
            ostring += decimal2words(istring.replace(",", ""))
    elif "/" in istring:
        if is_decimal is True and istring.count("/") == 1:
            num, fra = istring.split("/")
            ostring += f" {decimal2words(num)} phần {decimal2words(fra)} "
        else:
            _string = istring.split("/")
            ostring = " trên ".join([decimal2words(x) for x in _string])
    else:
        ostring += decimal2words(istring)

    return ostring


def read_ndigit(istring: str) -> str:
    ostring = ""
    if istring.startswith("+"):
        ostring += "cộng "
    ostring += " ".join([smallnumread(v) for v in istring if v.isdigit()])

    return ostring


# Hàm đọc NSW dạng la mã
roman2int = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000, "IV": 4, "IX": 9, "XL": 40, "XC": 90, "CD": 400, "CM": 900}
def read_nroman(istring: str) -> str:
    i, ostring  = 0, 0
    while i < len(istring):
        if i + 1 < len(istring) and istring[i:i + 2] in roman2int:
            ostring += roman2int[istring[i:i + 2]]
            i += 2
        else:
            ostring += roman2int[istring[i]]
            i += 1

    return smallnumread(str(ostring))
