from constants.charset import PunctuationCharset, SymbolCharset


class EmailRegular:
    EMAIL_FORMULA = r"[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4})+"
    URL_FORMULA_LONG = r"((?:http(s)?:\/\/)|(www))[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\"\(\)\*\+,;=.]+"
    URL_FORMULA_SHORT = r"([\w.-]+(?:\.[\w\.-]+)+)?[\w\-\._~:/?#[\]@!\$&\"\(\)\*\+,;=.]+(\.(com|gov|vn|com|org|info|io|net|edu))+"
    URL_FORMULA = "|".join([URL_FORMULA_LONG, URL_FORMULA_SHORT])
    REGREX = [
        r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*",
    ]


class PunctuationRegular:
    READ_PUNCTUATION = "|\\".join(PunctuationCharset.READ)
    DURATION_PUNCTUATION = "|\\".join(PunctuationCharset.DURATION)
    PUNCTUATION = READ_PUNCTUATION + "|" + DURATION_PUNCTUATION


class SymbolRegular:
    REGEX_SYMBOL = "|".join(list(SymbolCharset.SYMBOL))


class WebsiteRegular:
    REGREX = [
        r"(?i)\b(https?:\/\/|ftp:\/\/|www\.|[^\s:=]+@www\.)?((\w+)\.)+(?:com|au\.uk|co\.in|net|org|info|coop|int|co\.uk|org\.uk|ac\.uk|uk)([\.\/][^\s]*)*([^(w|\d)]|$)",
        r"(?i)\b((https?:\/\/|ftp:\/\/|sftp:\/\/|www\.|[^\s:=]+@www\.))(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\d]+-[a-z\d])*[a-z\d]+)(?:\.(?:[a-z\d]+-?)*[a-z\d]+)*(?:\.(?:[a-z]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?([^(w|\d)]|$)",
    ]


class DateRegular:
    DOUBLE_REGREX_TYPE_1 = [
        r"(từ|ngày) ([0-3]?[0-9][.\/][01]?\d[.\/][12]\d{3})\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d[.\/][12]\d{3})\b",
        r"(?i)(từ|ngày) ([0-3]?[0-9][.\/][01]?\d)\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d[.\/][12]\d{3})\b",
        r"(?i)(từ|ngày) ([0-3]?[0-9])\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d[.\/][12]\d{3})\b",
        r"(?i)(từ|ngày) ([0-3]?[0-9][.\/][01]?\d)\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d)\b",
        r"(?i)(từ|ngày) ([0-3]?[0-9])\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d)\b",
    ]
    DOUBLE_REGREX_TYPE_2 = [
        r"([0-3]?[0-9][\/][01]?\d)\s?(-|đến|và)\s?([0-3]?[0-9][\/][01]?\d)\b",
        r"([0-3]?[0-9])\s?(-|đến|và)\s?([0-3]?[0-9][\/][01]?\d)\b",
    ]
    DOUBLE_REGREX_TYPE_3 = [
        r"(?i)(từ|tháng) ([01]?\d[.\/][12]\d{3})\s?(-|đến|và)\s?([01]?\d[.\/][12]\d{3})\b",
        r"(?i)(từ|tháng) ([01]?\d)\s?(-|đến|và)\s?([01]?\d[.\/][12]\d{3})\b",
    ]
    SINGLE_REGREX_TYPE_1 = [
        r"(?i)\b[0-3]?[0-9]\s?\/\s?[01]?\d\s?\/\s?[12]\d{3}\b",
        r"(?i)\b[0-3]?[0-9]\s?-\s?[01]?\d\s?-\s?[12]\d{3}\b",
        r"(?i)\b[0-3]?[0-9]\s?\.\s?[01]?\d\s?\.\s?[12]\d{3}\b",
    ]
    SINGLE_REGREX_TYPE_2 = [
        r"(?i)\b\s?(quý|đoạn)\s+([IVX]+[\s\-\/][12]\d{3})\s?(-|đến|và)\s?([IVX]+[\s\-\/][12]\d{3})\b",
        r"(?i)\b\s?(quý|đoạn)\s+([IVX]+[\s\-\/][12]\d{3})\s?(-|đến|và)\s?([12]\d{3})\b",
        r"(?i)\b\s?(quý|đoạn)\s+([IVX]+[\s\-\/][12]\d{3})\b",
    ]
    SINGLE_REGREX_TYPE_3 = [
        r"(?i)\b(ngày|sáng|trưa|chiều|tối|đêm|hôm|nay|mai|hai|ba|tư|năm|sáu|bảy|nhật|qua|lúc|sáng sớm|lễ|công viên)\s+(\(?[0-3]?[0-9]\s?[\/.-]\s?[01]?\d)\b"
    ]
    MONTH_REGREX = [r"(?i)(tháng|quý) (\d{1,2}\s?[\/.-]\s?\d{4})\b"]


class TimeRegular:
    REGREX = [
        r"(?i)\b(\d{1,2})[h]?(\d{1,2})?\s?(-)\s?(\d{1,2})[h](\d{1,2})\b",
        r"(?i)\b\d{1,2}[h]\d{1,2}[m]?\b\s?(-?)\s?",
        r"(?i)\b\d{1,2}[h]\b\s?(-?)\s?",
        r"(?i)\b(?:2[0-4]|[01]?[0-9])[:h][0-5][0-9][:m]?[0-5][0-9][s]?\b(\s?-?\s?)",
        r"(?i)\b(?:2[0-4]|[01]?[0-9])[:h][0-5][0-9][m]?\b\s?(-?)\s?",
    ]


class ScoreRegular:
    SCORE_REGREX = [
        r"(?i)([đ]ội hình) \b\d\s?-\s?\d\s?-\s?\d(-\s?\d)?\b",
        r"(?i)([t]ỉ số|dẫn|thắng|thua|hòa) \b\d{1,2}\s?[-|]\s?\d{1,2}\b",
    ]
    UNDER_REGREX = [r"(?i)\b[u][.]?\d{2}\b"]


class LocationRegular:
    POLITICAL_REGREX = [
        r"(?i)\b(kp|q|p|h|tx|tp|x)\s?[.]\s?\d+",
    ]
    STREET_REGREX = [
        r"(?i)\b(đường|số nhà|nhà|địa chỉ|tọa lạc|xã|thôn|ấp|khu phố|căn hộ|cư xá|Đ\/c)[\s:]\s?\d+(/\d+)?\b",
    ]
    LICENSE_REGREX = [
        r"(?i)\b(\d{2})([A-Za-z])\s?(-)\s?(\d{3}\.?\d{2})\b",
    ]


class MeansureRegular:
    REGREX_TYPE_1 = [
        r"(?i)\b(\d+(?:\.\d{3})+(?:,\d+)?)\s?([°|A-Za-z]+[2|3]?)(?:\/([A-Za-z]+[2|3]?))?(?:\b|$)(\s?-?)",
        r"(?i)\b(\d+(?:,\d{3})+(?:\.\d+)?)\s?([°|A-Za-z]+[2|3]?)(?:\/(A-Za-z+[2|3]?))?(?:\b|$)(\s?-?)",
        r"(?i)\b(\d+(?:,\d+))\s?([°|A-Za-z]+[2|3]?)(?:\/(A-Za-z+[2|3]?))?(?:\b|$)(\s?-?)",
        r"(?i)\b(\d+(?:\.\d+)?)\s?([°|A-Za-z]+[2|3]?)(?:\/(A-Za-z+[2|3]?))?(?:\b|$)(\s?-?)",
    ]
    REGREX_TYPE_2 = [
        r"(?i)(?:\b|^)(\d+(?:,\d+))\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)?(\s?-\s?)(\d+(?:,\d+))\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)",
        r"(?i)(?:\b|^)(\d+(?:\.\d{3})+(?:,\d+)?)\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)",
        r"(?i)(?:\b|^)(\d+(?:,\d{3})+(?:\.\d+)?)\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)",
        r"(?i)(?:\b|^)(\d+(?:,\d+))\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)",
        r"(?i)(?:\b|^)(\d+(?:\.\d+)?)\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)",
    ]


class RomanRegular:
    REGREX = [
        r"\b(thứ|lần|kỷ|kỉ|kì|kỳ|khoá|cấp|độ|đoạn)\s+([V|I|X]{1,5})\b",
    ]


class PhoneRegular:
    REGREX = [
        r"([^(\w|\d|\.)]|^)((\+\d{1,3})|0)[-\s.]?\d{1,3}[-\s.]?\d{3}[-\s.]?\d{4}\b",
        r"([^(\w|\d|\.)]|^)((\+\d{1,3})|0)[-\s.]?\d{2,3}[-\s.]?\d{2}[- .]?\d{2}[- .]?\d{2}\b",
        r"([^(\w|\d|\.)]|^)((\+\d{1,3})|0)[-\s.]?\d{1,3}[-\s.]?\d{1,2}[-\s.]?\d{2,3}[-\s.]?\d{3}\b",
        r"\b1[89]00[\s\.]?[\d\s\.]{4,8}\b",
    ]


class ContinuosRegular:
    REGREX = [
        r"(?i)\b\d+(\.\d+)\s?(\-)\s?\d+(\.\d+)?",
        r"(?i)\b\d+(\,\d+)\s?(\-)\s?\d+(\,\d+)?",
        r"(?i)\b\d\s?(\-)\s?\d+",
    ]
