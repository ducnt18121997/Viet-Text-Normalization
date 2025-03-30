import re
import unidecode
import unicodedata
import constants
from num2words import num2words
from utils.helper import get_separator, split_num_word, is_number


class NumberReader:
    @staticmethod
    def big_number(istring: str, index=0) -> str:
        """Đọc số lớn hơn 9 tỷ"""
        if len(istring) <= 9:
            return NumberReader.small_number(istring)
        else:
            index += 1
            big = istring[:-9]
            small = istring[-9:]
            return (
                NumberReader.big_number(big, index + 1)
                + " "
                + "tỷ " * index
                + " "
                + NumberReader.small_number(small)
            )

    @staticmethod
    def small_number(istring: str) -> str:
        """Đọc số nhỏ hơn 1000"""
        number_value = int(istring)
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

    @staticmethod
    def decimal_number(istring: str) -> str:
        """Đọc số thập phân"""
        istring = unicodedata.normalize("NFKC", istring.strip())
        if len(istring) <= 9:
            return NumberReader.small_number(istring)
        else:
            return NumberReader.big_number(istring)

    @staticmethod
    def roman(istring: str) -> str:
        """Đọc số la mã"""
        i, ostring = 0, 0
        while i < len(istring):
            if (
                i + 1 < len(istring)
                and istring[i : i + 2] in constants.RomanCharset.READER
            ):
                ostring += constants.RomanCharset.READER[istring[i : i + 2]]
                i += 2
            else:
                ostring += constants.RomanCharset.READER[istring[i]]
                i += 1

        return NumberReader.small_number(str(ostring))

    @staticmethod
    def number(istring: str, is_decimal: bool = True) -> str:
        """Đọc số bất kỳ"""
        ostring = ""
        if istring.startswith("-"):
            ostring += " âm "
            istring = istring[1:]
        elif "+" in istring or "-" in istring:
            _string = istring.replace("-", " trừ ").replace("+", " cộng ").split()
            ostring = " ".join(
                [
                    NumberReader.number(x) if x not in ["cộng", "trừ"] else x
                    for x in _string
                ]
            )
        elif "." in istring and "," in istring:
            nnum_arr = istring.split(",")
            ostring += " phẩy ".join(
                [
                    NumberReader.number(nnum_arr[i], is_decimal=False)
                    for i in range(len(nnum_arr))
                ]
            )
        elif "," in istring:
            if (
                is_decimal is True
                and istring.count(",") == 1
                and not istring.endswith("00")
            ):
                num, fra = istring.split(",")
                ostring += f" {NumberReader.number(num)} phẩy {NumberReader.number(fra) if len(fra) < 3 else NumberReader.number(fra)}"
            else:
                ostring += NumberReader.number(istring.replace(",", ""))
        elif "." in istring:
            istring = istring.replace(".", ",")
            if (
                is_decimal is True
                and istring.count(",") == 1
                and len(istring.split(",")[-1]) != 3
            ):
                num, fra = istring.split(",")
                ostring += f" {NumberReader.number(num)} phẩy {NumberReader.number(fra) if len(fra) < 3 else NumberReader.number(fra)}"
            else:
                ostring += NumberReader.number(istring.replace(",", ""))
        elif "/" in istring:
            if is_decimal is True and istring.count("/") == 1:
                num, fra = istring.split("/")
                ostring += (
                    f" {NumberReader.number(num)} phần {NumberReader.number(fra)} "
                )
            else:
                _string = istring.split("/")
                ostring = " trên ".join([NumberReader.number(x) for x in _string])
        else:
            ostring += NumberReader.small_number(istring)

        return ostring

    @staticmethod
    def digit(istring: str) -> str:
        """Đọc số dạng ký tự"""
        ostring = ""
        if istring.startswith("+"):
            ostring += "cộng "
        ostring += " ".join(
            [NumberReader.small_number(v) for v in istring if v.isdigit()]
        )

        return ostring


class DateReader:
    @staticmethod
    def date(istring: str) -> str:
        separator = get_separator(istring)
        d, m, y = [v for v in istring.split(separator)]
        ostring = (
            f" {NumberReader.small_number(d)} tháng tư năm {NumberReader.small_number(y)} "
            if int(m) == 4
            else f" {NumberReader.small_number(d)} tháng {NumberReader.small_number(m)} năm {NumberReader.small_number(y)} "
        )

        return ostring

    @staticmethod
    def day(istring: str) -> str:
        if all(c.isdigit() for c in istring):
            return NumberReader.small_number(istring)

        separator = get_separator(istring)
        if istring.count(separator) == 2:
            return DateReader.date(istring)

        d, m = [v for v in istring.split(separator)]
        ostring = (
            f" {NumberReader.small_number(d)} tháng tư "
            if int(m) == 4
            else f" {NumberReader.small_number(d)} tháng {NumberReader.small_number(m)} "
        )

        return ostring

    @staticmethod
    def month(istring: str, is_quarter: bool = False) -> str:
        if all(c.isdigit() for c in istring):
            return NumberReader.small_number(istring)
        if all(not c.isdigit() for c in istring):
            return NumberReader.roman(istring)

        separator = get_separator(istring)
        m, y = istring.split(separator)
        ostring = f" {NumberReader.roman(m) if is_quarter is True else NumberReader.small_number(m)} năm {NumberReader.small_number(y)} "

        return ostring


class TimeReader:
    @staticmethod
    def time(istring: str) -> str:
        # type 1: xx:xx:xx
        if ":" in istring:
            _string = istring.split(":")
            if len(_string) == 2:
                h, m = _string
                ostring = f" {NumberReader.small_number(h)} giờ "
                if int(m.strip()) != 0:
                    ostring += f" {NumberReader.small_number(m)} phút "
            elif len(_string) == 3:
                h, m, s = _string
                ostring = f" {NumberReader.small_number(h)} giờ {NumberReader.small_number(m)} phút "
                if int(s.strip()) != 0:
                    ostring += f" {NumberReader.small_number(s)} giây"
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
                ostring = [
                    x if not x.isdigit() else NumberReader.small_number(x)
                    for i, x in enumerate(tstring)
                ]
            else:
                ostring = [
                    x if not x.isdigit() else NumberReader.small_number(x)
                    for i, x in enumerate(tstring[:-1])
                ]
                if int(tstring[-1]) != 0 or len(tstring) == 1:
                    ostring.append(NumberReader.small_number(tstring[-1]))
            ostring = " ".join(ostring)

        return ostring


class WordReader:
    @staticmethod
    def upper(istring: str, use_dictionary: bool = True) -> str:
        # đọc từ điển mapping từ viết tất
        if (
            use_dictionary is True
            and istring in constants.VietnameseAbbreviation.SINGLE_ABBREVIATION
        ):
            ostring = constants.VietnameseAbbreviation.SINGLE_ABBREVIATION[istring]
        # đọc từ điển mapping từ viết hoa đọc bình thường
        elif istring in constants.VietnameseAbbreviation.DOUBLE_ABBREVIATION:
            ostring = constants.VietnameseAbbreviation.DOUBLE_ABBREVIATION[istring]
        # đọc theo tiếng việt
        elif istring.lower() in constants.VietnameseWord.WORDS:
            ostring = istring.lower()
        elif "." in istring:
            istring = unidecode.unidecode(istring).replace(".", " ").strip().split()
            ostring = " ".join([WordReader.upper(s) for s in istring])
        # đọc từ UPPER ko xác định
        else:
            if (
                len(istring) <= 6
                or "Ư" in istring
                or all(s not in "AEOIU".upper() for s in istring)
            ):
                ostring = " ".join(
                    [
                        constants.VietnameseCharset.READER[ch]
                        for ch in istring
                        if ch in constants.VietnameseCharset.READER
                    ]
                )
            else:
                ostring = WordReader.lower(istring.lower())

        return ostring

    @staticmethod
    def lower(istring: str) -> str:
        if istring.endswith("."):  # maybe <EOS>
            return f" {WordReader.lower(istring[: -1])} {istring[-1]} "
        if "-" in istring:
            return " ".join([WordReader.lower(x) for x in istring.split("-") if x])
        # dọc tên ngân hàng (bank)
        elif istring.endswith("bank"):
            ostring = f"{WordReader.lower(istring[: -4])} banh"
        # đọc từ tiếng anh default
        else:
            ostring = (
                unicodedata.normalize("NFD", istring).encode("ascii", "ignore").decode()
            )

        return ostring

    @staticmethod
    def number(istring: str) -> str:
        if istring.endswith("."):  # maybe <EOS>
            return f" {WordReader.number(istring[: -1])} {istring[-1]} "
        elif "+" in istring or istring.startswith("-"):
            ostring = f" {'cộng' if istring[0] == '+' else 'trừ'} {WordReader.number(istring[1: ])} "
        elif is_number(istring, [".", ","]):
            _string = istring.replace("+", " cộng ").replace("-", " trừ ").split()
            ostring = " ".join(
                [
                    NumberReader.number(x) if x not in ["cộng", "trừ"] else x
                    for x in _string
                ]
            )
        elif "-" in istring or ":" in istring:
            _string = istring.replace("-", " ").replace(":", " ").split()
            ostring = " ".join([WordReader.number(x) for x in _string])
        elif "/" in istring:
            if re.fullmatch(r"\b(2[0-4]|1[0-9]|0?[1-9])\/(1[0-2]|0?[1-9])\b", istring):
                ostring = DateReader.day(istring)
            elif re.fullmatch(r"\b(1[0-2]|0?[1-9])\/([12]\d{3})\b", istring):
                ostring = DateReader.month(istring)
            else:
                _string = istring.split("/")
                ostring = " trên ".join(
                    NumberReader.number(_str) for _str in _string if _str
                )
        elif istring[-1] in constants.CurrencyCharset.CURRENCY:
            ostring = f"{NumberReader.number(istring[: -1])} {constants.CurrencyCharset.READER[istring[-1]]}"
        elif istring[0] in constants.CurrencyCharset.CURRENCY:
            ostring = f"{NumberReader.number(istring[1: ])} {constants.CurrencyCharset.READER[istring[0]]}"
        elif istring in constants.CurrencyCharset.CURRENCY:
            ostring = constants.CurrencyCharset.READER[istring]
        else:
            _string = split_num_word(istring).split()
            ostring = []
            for x in _string:
                if x.isdigit():
                    ostring.append(
                        NumberReader.number(x) if x[0] != "0" else NumberReader.digit(x)
                    )
                elif x.lower() in constants.VietnameseWord.WORDS:
                    ostring.append(x.lower())
                elif x.isupper():
                    ostring.append(WordReader.upper(x, use_dictionary=False))
                else:
                    ostring.append(WordReader.lower(x))
            ostring = " ".join(ostring)

        return ostring
