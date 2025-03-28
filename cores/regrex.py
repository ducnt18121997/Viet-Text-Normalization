import re
from cores.reader import DateReader, TimeReader, NumberReader
from constants import regular, word


class RegrexNormalize:
    @staticmethod
    def whitespace(text: str) -> str:
        """Normalize whitespace via regex"""
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def website(text: str) -> str:
        """Normalize website via regex"""
        # TODO: Implement this function
        for _reg in regular.WebsiteRegular.REGREX:
            for match in re.compile(_reg).finditer(text):
                mtxt = f" link đính kèm "
                text = text.replace(match.group(), mtxt)
        return text

    @staticmethod
    def mail(text: str) -> str:
        """Normalize mail via regex"""
        # TODO: Implement this function
        for _reg in regular.EmailRegular.REGREX:
            for match in re.compile(_reg).finditer(text):
                mtxt = f" link đính kèm "
                text = text.replace(match.group(), mtxt)
        return text

    @staticmethod
    def date(text: str) -> str:
        """Normalize date via regex"""
        # TODO: Implement this function
        for _reg in regular.DateRegular.DOUBLE_REGREX_TYPE_1:
            for match in re.compile(_reg).finditer(text):
                _tmp = [m.replace(".", "/") for m in match.groups() if m is not None]
                if _tmp[1].endswith(".0") or _tmp[3].endswith(".0"):
                    continue  # Exception case: `Độ cao sóng lớn nhất từ 1.0 - 2.0 m .` `Sóng biển cao nhất từ 1.0 - 2.0 m .`,...
                assert (
                    len(_tmp) == 4
                ), f"matching group length should be 4, given {' '.join(_tmp)}"
                mtxt = f" {_tmp[0]} {'ngày' if _tmp[0] == 'từ' else ''} {DateReader.day(_tmp[1])} {'đến' if _tmp[2] == '-' else _tmp[2]} ngày {DateReader.day(_tmp[3])} "

                text = text.replace(match.group(), mtxt)

        for _reg in regular.DateRegular.DOUBLE_REGREX_TYPE_2:
            for match in re.compile(_reg).finditer(text):
                _tmp = [m for m in match.groups() if m is not None]
                assert (
                    len(_tmp) == 3
                ), f"matching group length should be 4, given {' '.join(_tmp)}"
                mtxt = f" ngày {DateReader.day(_tmp[0])} {'đến' if _tmp[1] == '-' else _tmp[1]} ngày {DateReader.day(_tmp[2])} "

                text = text.replace(match.group(), mtxt)

        for _reg in regular.DateRegular.DOUBLE_REGREX_TYPE_3:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.groups()
                assert (
                    len(_tmp) == 4
                ), f"matching group length should be 4, given {' '.join(_tmp)}"
                mtxt = f" {_tmp[0]} {'tháng' if _tmp[0] == 'từ' else ''} {DateReader.month(_tmp[1])} {'đến' if _tmp[2] == '-' else _tmp[2]} tháng {DateReader.month(_tmp[3])} "

                text = text.replace(match.group(), mtxt)

        for _reg in regular.DateRegular.SINGLE_REGREX_TYPE_1:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.group().strip()
                mtxt = f" {DateReader.date(_tmp)} "
                text = text.replace(match.group(), mtxt)

        for _reg in regular.DateRegular.SINGLE_REGREX_TYPE_2:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.groups()
                assert len(_tmp) in [
                    2,
                    4,
                ], f"matching group length should be 2 or 4, given {' '.join(_tmp)}"
                mtxt = f" {_tmp[0]} {DateReader.month(_tmp[1].replace(' ', '-'), is_quarter=True)} "
                if len(_tmp) == 4:
                    mtxt += f"{'đến' if _tmp[2] == '-' else _tmp[2]} năm {DateReader.month(_tmp[3], is_quarter=True)} "
                text = text.replace(match.group(), mtxt)

        for _reg in regular.DateRegular.SINGLE_REGREX_TYPE_3:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.groups()
                mtxt = f" {_tmp[0]} {DateReader.day(_tmp[1].replace('(', '').replace(' ', ''))} "
                text = text.replace(match.group(), mtxt)

        for _reg in regular.DateRegular.MONTH_REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.groups()
                mtxt = f" {_tmp[0]} {DateReader.month(_tmp[1].replace(' ', ''))} "
                text = text.replace(match.group(), mtxt)

    @staticmethod
    def time(text: str) -> str:
        """Normalize time via regex"""
        for _reg in regular.TimeRegular.REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.group().strip().split("-")
                if len(_tmp) == 2:
                    mtxt = f" {TimeReader.time(_tmp[0].replace(' ', ''))} đến {TimeReader.time(_tmp[1].replace(' ', ''))} "
                else:
                    mtxt = " - ".join(
                        [TimeReader.time(x.replace(" ", "")) if x else x for x in _tmp]
                    )
                text = text.replace(match.group(), mtxt)

            for match in re.compile(_reg).finditer(text):
                _tmp = match.group().strip()
                if _tmp[-1] == "-":
                    mtxt = f" {TimeReader.time(_tmp[:-1].replace(' ', ''))} {_tmp[-1]} "
                else:
                    mtxt = f" {TimeReader.time(_tmp.replace(' ', ''))} "
                text = text.replace(match.group(), mtxt)

    @staticmethod
    def score(text: str) -> str:
        """Normalize score via regex"""
        for _reg in regular.ScoreRegular.SCORE_REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.group().replace("-", " ").split()
                mtxt = " ".join(
                    [NumberReader.number(x) if x.isdigit() else x for x in _tmp]
                )
                text = text.replace(match.group(), mtxt)
        for _reg in regular.ScoreRegular.UNDER_REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.group()
                mtxt = f" {_tmp[0]} {NumberReader.number(_tmp[1: ].strip(), is_decimal=False)}"
                text = text.replace(match.group(), mtxt)

    @staticmethod
    def location(text: str) -> str:
        """Normalize location via regex"""
        for _reg in regular.LocationRegular.POLITICAL_REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.group().upper().replace(".", " ").split()
                mtxt = f" {word.VN_LOCATION[_tmp[0].upper()]} {NumberReader.number(_tmp[1])} "
                text = text.replace(match.group(), mtxt)
        for _reg in regular.LocationRegular.STREET_REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.group()
                for i in range(len(_tmp)):
                    if _tmp[i].isdigit():
                        break
                mtxt = (
                    f" {_tmp[: i]} {NumberReader.number(_tmp[i: ], is_decimal=False)} "
                )
                text = text.replace(match.group(), mtxt)
        for _reg in regular.LocationRegular.LICENSE_REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.groups()
                mtxt = f" {NumberReader.number(_tmp[0])} {_tmp[1]} {NumberReader.number(_tmp[3].replace('.', ''))} "
                text = text.replace(match.group(), mtxt)

    def meansure(text: str) -> str:
        """Normalize meansure via regex"""
        for _reg in regular.MeansureRegular.REGREX_TYPE_1:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.groups()
                mtxt = f" {NumberReader.number(_tmp[0], is_decimal=True)} "
                mtxt += f"{word.VN_LOCATION[_tmp[1]] if _tmp[1] in word.VN_LOCATION else _tmp[1]} {'trên' if '/' in match.group() else ''}"
                if _tmp[2] is not None:
                    mtxt += f"{word.VN_LOCATION[_tmp[2]] if _tmp[2] in word.VN_LOCATION else _tmp[2]} "
                mtxt += f"{_tmp[3]} "
                text = text.replace(match.group(), mtxt)

        for _reg in regular.MeansureRegular.REGREX_TYPE_2:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.groups()
                if len(_tmp) == 5:
                    # mtxt = f" {read_nnumber(_tmp[0], is_decimal=True)} đến {read_nnumber(_tmp[2], is_decimal=True)} {dict_currency_unit[_tmp[3]] if _tmp[3] in dict_currency_unit else _tmp[3]} {_tmp[4]}"
                    mtxt = []
                    for word in _tmp:
                        if word is not None and word[0].isdigit():
                            mtxt.append(NumberReader.number(word, is_decimal=True))
                        elif word in word.VN_LOCATION:
                            mtxt.append(word.VN_LOCATION[word])
                        else:
                            mtxt.append(word)
                    mtxt = " ".join([ch for ch in mtxt if ch is not None]).replace(
                        "-", "đến"
                    )
                else:
                    mtxt = f" {NumberReader.number(_tmp[0], is_decimal=True)} {word.VN_LOCATION[_tmp[1]] if _tmp[1] in word.VN_LOCATION else _tmp[1]} {_tmp[2]}"
                text = text.replace(match.group(), mtxt)

    @staticmethod
    def roman(text: str) -> str:
        """Normalize roman via regex"""
        for _reg in regular.RomanRegular.REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.groups()
                mtxt = f" {_tmp[0]} {NumberReader.roman(_tmp[1].upper())} "
                text = text.replace(match.group(), mtxt)

    @staticmethod
    def phone(text: str) -> str:
        """Normalize phone via regex"""
        for _reg in regular.PhoneRegular.REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.group()
                mtxt = NumberReader.number(_tmp)
                text = text.replace(match.group(), mtxt)

    @staticmethod
    def continuos(text: str) -> str:
        """Normalize continuos via regex"""
        for _reg in regular.ContinuosRegular.REGREX:
            for match in re.compile(_reg).finditer(text):
                _tmp = match.group().replace(" ", "")
                _sep = "/" if "/" in _tmp else "-"
                _tmp = _tmp.split(_sep)
                mtxt = f" {NumberReader.number(_tmp[0], is_decimal=True)} {'đến' if _sep == '-' else 'trên'} {NumberReader.number(_tmp[1], is_decimal=True)} "
                text = text.replace(match.group(), mtxt)


def normalize(text: str) -> str:
    text = RegrexNormalize.website(text)
    text = RegrexNormalize.mail(text)
    text = RegrexNormalize.date(text)
    text = RegrexNormalize.time(text)
    text = RegrexNormalize.score(text)
    text = RegrexNormalize.location(text)
    text = RegrexNormalize.meansure(text)
    text = RegrexNormalize.roman(text)
    text = RegrexNormalize.phone(text)
    text = RegrexNormalize.continuos(text)

    return text
