from constants.charset import PunctuationCharset, SymbolCharset


class EmailRegular:
    EMAIL_FORMULA = r"[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4})+"
    URL_FORMULA_LONG = r"((?:http(s)?:\/\/)|(www))[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\"\(\)\*\+,;=.]+"
    URL_FORMULA_SHORT = r"([\w.-]+(?:\.[\w\.-]+)+)?[\w\-\._~:/?#[\]@!\$&\"\(\)\*\+,;=.]+(\.(com|gov|vn|com|org|info|io|net|edu))+"
    URL_FORMULA = "|".join([URL_FORMULA_LONG, URL_FORMULA_SHORT])


class PunctuationRegular:
    REGEX_SKIP_PUNCTUATION = PunctuationCharset.REGEX_SKIP_PUNCTUATION
    REGEX_SILENT_PUNCTUATION = PunctuationCharset.REGEX_SILENT_PUNCTUATION
    REGEX_DURA_PUNCTUATION = PunctuationCharset.REGEX_DURA_PUNCTUATION
    REGEX_READ_PUNCTUATION = PunctuationCharset.REGEX_READ_PUNCTUATION


class SymbolRegular:
    REGEX_SYMBOL = "|".join(list(SymbolCharset.DICT_SYMBOL.keys()))
