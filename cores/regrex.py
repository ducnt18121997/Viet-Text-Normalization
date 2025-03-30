import re
import constants
from cores.reader import DateReader, TimeReader, NumberReader


class RegrexNormalize:
    @staticmethod
    def whitespace(text: str) -> str:
        """Normalize whitespace via regex"""
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def website(text: str) -> str:
        """Normalize website via regex"""
        # TODO: Implement this function
        for reg in constants.WebsiteRegular.REGREX:
            for match in re.compile(reg).finditer(text):
                mtxt = f" link đính kèm "
                text = text.replace(match.group(), mtxt)
        return text

    @staticmethod
    def mail(text: str) -> str:
        """Normalize mail via regex"""
        # TODO: Implement this function
        for reg in constants.EmailRegular.REGREX:
            for match in re.compile(reg).finditer(text):
                mtxt = f" link đính kèm "
                text = text.replace(match.group(), mtxt)
        return text

    @staticmethod
    def date(text: str) -> str:
        """Normalize date via regex"""
        # TODO: Implement this function
        for reg in constants.DateRegular.DOUBLE_REGREX_TYPE_1:
            for match in re.compile(reg).finditer(text):
                temp = [m.replace(".", "/") for m in match.groups() if m is not None]
                if temp[1].endswith(".0") or temp[3].endswith(".0"):
                    continue  # Exception case: `Độ cao sóng lớn nhất từ 1.0 - 2.0 m .` `Sóng biển cao nhất từ 1.0 - 2.0 m .`,...
                assert (
                    len(temp) == 4
                ), f"matching group length should be 4, given {' '.join(temp)}"
                mtxt = f" {temp[0]} {'ngày' if temp[0] == 'từ' else ''} {DateReader.day(temp[1])} {'đến' if temp[2] == '-' else temp[2]} ngày {DateReader.day(temp[3])} "

                text = text.replace(match.group(), mtxt)

        for reg in constants.DateRegular.DOUBLE_REGREX_TYPE_2:
            for match in re.compile(reg).finditer(text):
                temp = [m for m in match.groups() if m is not None]
                assert (
                    len(temp) == 3
                ), f"matching group length should be 4, given {' '.join(temp)}"
                mtxt = f" ngày {DateReader.day(temp[0])} {'đến' if temp[1] == '-' else temp[1]} ngày {DateReader.day(temp[2])} "

                text = text.replace(match.group(), mtxt)

        for reg in constants.DateRegular.DOUBLE_REGREX_TYPE_3:
            for match in re.compile(reg).finditer(text):
                temp = match.groups()
                assert (
                    len(temp) == 4
                ), f"matching group length should be 4, given {' '.join(temp)}"
                mtxt = f" {temp[0]} {'tháng' if temp[0] == 'từ' else ''} {DateReader.month(temp[1])} {'đến' if temp[2] == '-' else temp[2]} tháng {DateReader.month(temp[3])} "

                text = text.replace(match.group(), mtxt)

        for reg in constants.DateRegular.SINGLE_REGREX_TYPE_1:
            for match in re.compile(reg).finditer(text):
                temp = match.group().strip()
                mtxt = f" {DateReader.date(temp)} "
                text = text.replace(match.group(), mtxt)

        for reg in constants.DateRegular.SINGLE_REGREX_TYPE_2:
            for match in re.compile(reg).finditer(text):
                temp = match.groups()
                assert len(temp) in [
                    2,
                    4,
                ], f"matching group length should be 2 or 4, given {' '.join(temp)}"
                mtxt = f" {temp[0]} {DateReader.month(temp[1].replace(' ', '-'), is_quarter=True)} "
                if len(temp) == 4:
                    mtxt += f"{'đến' if temp[2] == '-' else temp[2]} năm {DateReader.month(temp[3], is_quarter=True)} "
                text = text.replace(match.group(), mtxt)

        for reg in constants.DateRegular.SINGLE_REGREX_TYPE_3:
            for match in re.compile(reg).finditer(text):
                temp = match.groups()
                mtxt = f" {temp[0]} {DateReader.day(temp[1].replace('(', '').replace(' ', ''))} "
                text = text.replace(match.group(), mtxt)

        for reg in constants.DateRegular.MONTH_REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.groups()
                mtxt = f" {temp[0]} {DateReader.month(temp[1].replace(' ', ''))} "
                text = text.replace(match.group(), mtxt)

        return text

    @staticmethod
    def time(text: str) -> str:
        """Normalize time via regex"""
        for reg in constants.TimeRegular.REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.group().strip().split("-")
                if len(temp) == 2:
                    mtxt = f" {TimeReader.time(temp[0].replace(' ', ''))} đến {TimeReader.time(temp[1].replace(' ', ''))} "
                else:
                    mtxt = " - ".join(
                        [TimeReader.time(x.replace(" ", "")) if x else x for x in temp]
                    )
                text = text.replace(match.group(), mtxt)

            for match in re.compile(reg).finditer(text):
                temp = match.group().strip()
                if temp[-1] == "-":
                    mtxt = f" {TimeReader.time(temp[:-1].replace(' ', ''))} {temp[-1]} "
                else:
                    mtxt = f" {TimeReader.time(temp.replace(' ', ''))} "
                text = text.replace(match.group(), mtxt)

        return text

    @staticmethod
    def score(text: str) -> str:
        """Normalize score via regex"""
        for reg in constants.ScoreRegular.SCORE_REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.group().replace("-", " ").split()
                mtxt = " ".join(
                    [NumberReader.number(x) if x.isdigit() else x for x in temp]
                )
                text = text.replace(match.group(), mtxt)
        for reg in constants.ScoreRegular.UNDER_REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.group()
                mtxt = f" {temp[0]} {NumberReader.number(temp[1: ].strip(), is_decimal=False)}"
                text = text.replace(match.group(), mtxt)

        return text

    @staticmethod
    def location(text: str) -> str:
        """Normalize location via regex"""
        for reg in constants.LocationRegular.POLITICAL_REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.group().upper().replace(".", " ").split()
                mtxt = f" {constants.VN_LOCATION[temp[0].upper()]} {NumberReader.number(temp[1])} "
                text = text.replace(match.group(), mtxt)
        for reg in constants.LocationRegular.STREET_REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.group()
                for i in range(len(temp)):
                    if temp[i].isdigit():
                        break
                mtxt = (
                    f" {temp[: i]} {NumberReader.number(temp[i: ], is_decimal=False)} "
                )
                text = text.replace(match.group(), mtxt)
        for reg in constants.LocationRegular.LICENSE_REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.groups()
                mtxt = f" {NumberReader.number(temp[0])} {temp[1]} {NumberReader.number(temp[3].replace('.', ''))} "
                text = text.replace(match.group(), mtxt)

        return text

    def meansure(text: str) -> str:
        """Normalize meansure via regex"""
        for reg in constants.MeansureRegular.REGREX_TYPE_1:
            for match in re.compile(reg).finditer(text):
                temp = match.groups()
                mtxt = f" {NumberReader.number(temp[0], is_decimal=True)} "
                mtxt += f"{constants.VietnameseLocation.LOCATION[temp[1]] if temp[1] in constants.VietnameseLocation.LOCATION else temp[1]} {'trên' if '/' in match.group() else ''}"
                if temp[2] is not None:
                    mtxt += f"{constants.VietnameseLocation.LOCATION[temp[2]] if temp[2] in constants.VietnameseLocation.LOCATION else temp[2]} "
                mtxt += f"{temp[3]} "
                text = text.replace(match.group(), mtxt)

        for reg in constants.MeansureRegular.REGREX_TYPE_2:
            for match in re.compile(reg).finditer(text):
                temp = match.groups()
                if len(temp) == 5:
                    # mtxt = f" {read_nnumber(temp[0], is_decimal=True)} đến {read_nnumber(temp[2], is_decimal=True)} {dict_currency_unit[temp[3]] if temp[3] in dict_currency_unit else temp[3]} {temp[4]}"
                    mtxt = []
                    for word in temp:
                        if word is not None and word[0].isdigit():
                            mtxt.append(NumberReader.number(word, is_decimal=True))
                        elif word in constants.VietnameseLocation.LOCATION:
                            mtxt.append(constants.VietnameseLocation.READER[word])
                        else:
                            mtxt.append(word)
                    mtxt = " ".join([ch for ch in mtxt if ch is not None]).replace(
                        "-", "đến"
                    )
                else:
                    mtxt = f" {NumberReader.number(temp[0], is_decimal=True)} {constants.VietnameseLocation.READER[temp[1]] if temp[1] in constants.VietnameseLocation.LOCATION else temp[1]} {temp[2]}"
                text = text.replace(match.group(), mtxt)

        return text

    @staticmethod
    def roman(text: str) -> str:
        """Normalize roman via regex"""
        for reg in constants.RomanRegular.REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.groups()
                mtxt = f" {temp[0]} {NumberReader.roman(temp[1].upper())} "
                text = text.replace(match.group(), mtxt)

        return text

    @staticmethod
    def phone(text: str) -> str:
        """Normalize phone via regex"""
        for reg in constants.PhoneRegular.REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.group()
                mtxt = NumberReader.number(temp)
                text = text.replace(match.group(), mtxt)

        return text

    @staticmethod
    def continuous(text: str) -> str:
        """Normalize continuos via regex"""
        for reg in constants.ContinuosRegular.REGREX:
            for match in re.compile(reg).finditer(text):
                temp = match.group().replace(" ", "")
                _sep = "/" if "/" in temp else "-"
                temp = temp.split(_sep)
                mtxt = f" {NumberReader.number(temp[0], is_decimal=True)} {'đến' if _sep == '-' else 'trên'} {NumberReader.number(temp[1], is_decimal=True)} "
                text = text.replace(match.group(), mtxt)

        return text


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
    text = RegrexNormalize.continuous(text)

    return text
