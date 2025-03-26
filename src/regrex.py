import re
from .modules.reading import *
from .config import (
    dict_vn_location,
    dict_base_unit,
    dict_currency_unit
)

class display_colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m' 
    GREEN = '\033[92m' 
    YELLOW = '\033[93m' 
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def normalize_by_regrex(text: str) -> str:
    reg_website = [
        r"(?i)\b(https?:\/\/|ftp:\/\/|www\.|[^\s:=]+@www\.)?((\w+)\.)+(?:com|au\.uk|co\.in|net|org|info|coop|int|co\.uk|org\.uk|ac\.uk|uk)([\.\/][^\s]*)*([^(w|\d)]|$)",
        r"(?i)\b((https?:\/\/|ftp:\/\/|sftp:\/\/|www\.|[^\s:=]+@www\.))(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\d]+-[a-z\d])*[a-z\d]+)(?:\.(?:[a-z\d]+-?)*[a-z\d]+)*(?:\.(?:[a-z]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?([^(w|\d)]|$)",
    ]
    reg_mail    = [
        r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*",
    ]
    for _reg in reg_mail + reg_website:
        for match in re.compile(_reg).finditer(text):
            mtxt = f" link đính kèm "
            text = text.replace(match.group(), mtxt)

    reg_date_from_to_11 = [
        r"(từ|ngày) ([0-3]?[0-9][.\/][01]?\d[.\/][12]\d{3})\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d[.\/][12]\d{3})\b",
        r"(?i)(từ|ngày) ([0-3]?[0-9][.\/][01]?\d)\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d[.\/][12]\d{3})\b",
        r"(?i)(từ|ngày) ([0-3]?[0-9])\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d[.\/][12]\d{3})\b",
        r"(?i)(từ|ngày) ([0-3]?[0-9][.\/][01]?\d)\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d)\b",
        r"(?i)(từ|ngày) ([0-3]?[0-9])\s?(-|đến|và)\s?([0-3]?[0-9][.\/][01]?\d)\b",
    ]
    reg_date_from_to_12 = [
        r"([0-3]?[0-9][\/][01]?\d)\s?(-|đến|và)\s?([0-3]?[0-9][\/][01]?\d)\b",
        r"([0-3]?[0-9])\s?(-|đến|và)\s?([0-3]?[0-9][\/][01]?\d)\b",
    ]
    reg_date_from_to_2 = [
        r"(?i)(từ|tháng) ([01]?\d[.\/][12]\d{3})\s?(-|đến|và)\s?([01]?\d[.\/][12]\d{3})\b",
        r"(?i)(từ|tháng) ([01]?\d)\s?(-|đến|và)\s?([01]?\d[.\/][12]\d{3})\b",
    ]
    for _reg in reg_date_from_to_11:
        for match in re.compile(_reg).finditer(text):
            _tmp = [m.replace(".", "/") for m in match.groups() if m is not None]
            if _tmp[1].endswith(".0") or _tmp[3].endswith(".0"): continue # Exception case: `Độ cao sóng lớn nhất từ 1.0 - 2.0 m .` `Sóng biển cao nhất từ 1.0 - 2.0 m .`,...
            assert len(_tmp) == 4, f"matching group length should be 4, given {' '.join(_tmp)}"
            mtxt = f" {_tmp[0]} {'ngày' if _tmp[0] == 'từ' else ''} {read_nday(_tmp[1])} {'đến' if _tmp[2] == '-' else _tmp[2]} ngày {read_nday(_tmp[3])} "
            
            text = text.replace(match.group(), mtxt)
    for _reg in reg_date_from_to_12:
        for match in re.compile(_reg).finditer(text):
            _tmp = [m for m in match.groups() if m is not None]
            assert len(_tmp) == 3, f"matching group length should be 4, given {' '.join(_tmp)}"
            mtxt = f" ngày {read_nday(_tmp[0])} {'đến' if _tmp[1] == '-' else _tmp[1]} ngày {read_nday(_tmp[2])} "
            
            text = text.replace(match.group(), mtxt)
    for _reg in reg_date_from_to_2:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.groups()
            assert len(_tmp) == 4, f"matching group length should be 4, given {' '.join(_tmp)}"
            mtxt = f" {_tmp[0]} {'tháng' if _tmp[0] == 'từ' else ''} {read_nmon(_tmp[1])} {'đến' if _tmp[2] == '-' else _tmp[2]} tháng {read_nmon(_tmp[3])} "
            
            text = text.replace(match.group(), mtxt)
    
    reg_date_1 = [
        r"(?i)\b[0-3]?[0-9]\s?\/\s?[01]?\d\s?\/\s?[12]\d{3}\b",
        r"(?i)\b[0-3]?[0-9]\s?-\s?[01]?\d\s?-\s?[12]\d{3}\b",
        r"(?i)\b[0-3]?[0-9]\s?\.\s?[01]?\d\s?\.\s?[12]\d{3}\b",
    ]
    reg_date_2 = [
        r"(?i)\b\s?(quý|đoạn)\s+([IVX]+[\s\-\/][12]\d{3})\s?(-|đến|và)\s?([IVX]+[\s\-\/][12]\d{3})\b",
        r"(?i)\b\s?(quý|đoạn)\s+([IVX]+[\s\-\/][12]\d{3})\s?(-|đến|và)\s?([12]\d{3})\b",
        r"(?i)\b\s?(quý|đoạn)\s+([IVX]+[\s\-\/][12]\d{3})\b",
    ]
    reg_date_3 = [
        r"(?i)\b(ngày|sáng|trưa|chiều|tối|đêm|hôm|nay|mai|hai|ba|tư|năm|sáu|bảy|nhật|qua|lúc|sáng sớm|lễ|công viên)\s+(\(?[0-3]?[0-9]\s?[\/.-]\s?[01]?\d)\b"
    ]
    reg_month_1 = [
        r"(?i)(tháng|quý) (\d{1,2}\s?[\/.-]\s?\d{4})\b"
    ]
    for _reg in reg_date_1:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.group().strip()
            mtxt = f" {read_ndate(_tmp)} "
            text = text.replace(match.group(), mtxt)
    for _reg in reg_date_2:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.groups()
            assert len(_tmp) in [2, 4], f"matching group length should be 2 or 4, given {' '.join(_tmp)}"
            mtxt = f" {_tmp[0]} {read_nmon(_tmp[1].replace(' ', '-'), is_quarter=True)} "
            if len(_tmp) == 4: 
                mtxt += f"{'đến' if _tmp[2] == '-' else _tmp[2]} năm {read_nmon(_tmp[3], is_quarter=True)} "
            text = text.replace(match.group(), mtxt)
    for _reg in reg_date_3:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.groups()
            mtxt = f" {_tmp[0]} {read_nday(_tmp[1].replace('(', '').replace(' ', ''))} "
            text = text.replace(match.group(), mtxt)
    for _reg in reg_month_1:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.groups()
            mtxt = f" {_tmp[0]} {read_nmon(_tmp[1].replace(' ', ''))} "
            text = text.replace(match.group(), mtxt)
    
    reg_time_1 = [
        r"(?i)\b(\d{1,2})[h]?(\d{1,2})?\s?(-)\s?(\d{1,2})[h](\d{1,2})\b",
        r"(?i)\b\d{1,2}[h]\d{1,2}[m]?\b\s?(-?)\s?",
        r"(?i)\b\d{1,2}[h]\b\s?(-?)\s?",
        r"(?i)\b(?:2[0-4]|[01]?[0-9])[:h][0-5][0-9][:m]?[0-5][0-9][s]?\b(\s?-?\s?)",
        r"(?i)\b(?:2[0-4]|[01]?[0-9])[:h][0-5][0-9][m]?\b\s?(-?)\s?",
    ]
    for _reg in reg_time_1:
        for match in re.compile(_reg + _reg).finditer(text):
            _tmp = match.group().strip().split("-")
            if len(_tmp) == 2:
                mtxt = f" {read_ntime(_tmp[0].replace(' ', ''))} đến {read_ntime(_tmp[1].replace(' ', ''))} "
            else:
                mtxt = " - ".join([read_ntime(x.replace(' ', '')) if x else x for x in _tmp])
            text = text.replace(match.group(), mtxt)

        for match in re.compile(_reg).finditer(text):
            _tmp = match.group().strip()
            if _tmp[-1] == "-":
                mtxt = f" {read_ntime(_tmp[:-1].replace(' ', ''))} {_tmp[-1]} "
            else:
                mtxt = f" {read_ntime(_tmp.replace(' ', ''))} "
            text = text.replace(match.group(), mtxt)

    reg_football_1 = [
        r"(?i)([đ]ội hình) \b\d\s?-\s?\d\s?-\s?\d(-\s?\d)?\b",
        r"(?i)([t]ỉ số|dẫn|thắng|thua|hòa) \b\d{1,2}\s?[-|]\s?\d{1,2}\b",
    ]
    reg_under_1 = [
        r"(?i)\b[u][.]?\d{2}\b"
    ]
    for _reg in reg_football_1:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.group().replace("-", " ").split()
            mtxt = " ".join([smallnumread(x) if x.isdigit() else x for x in _tmp])
            text = text.replace(match.group(), mtxt)
    for _reg in reg_under_1:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.group()
            mtxt = f" {_tmp[0]} {read_nnumber(_tmp[1: ].strip(), is_decimal=False)}"
            text = text.replace(match.group(), mtxt)

    reg_political_1 = [
        r"(?i)\b(kp|q|p|h|tx|tp|x)\s?[.]\s?\d+",
    ]
    reg_street_1 = [
        r"(?i)\b(đường|số nhà|nhà|địa chỉ|tọa lạc|xã|thôn|ấp|khu phố|căn hộ|cư xá|Đ\/c)[\s:]\s?\d+(/\d+)?\b",
    ]
    reg_license  = [
        r"(?i)\b(\d{2})([A-Za-z])\s?(-)\s?(\d{3}\.?\d{2})\b",
    ]
    for _reg in reg_political_1:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.group().upper().replace(".", " ").split()
            mtxt = f" {dict_vn_location[_tmp[0].upper()]} {smallnumread(_tmp[1])} "
            text = text.replace(match.group(), mtxt)
    for _reg in reg_street_1:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.group()
            for i in range(len(_tmp)): 
                if _tmp[i].isdigit(): break
            mtxt = f" {_tmp[: i]} {read_nnumber(_tmp[i: ], is_decimal=False)} "
            text = text.replace(match.group(), mtxt)
    for _reg in reg_license:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.groups()
            mtxt = f" {read_nnumber(_tmp[0])} {_tmp[1]} {read_ndigit(_tmp[3].replace('.', ''))} "
            text = text.replace(match.group(), mtxt)

    reg_meansure_1 = [
        r"(?i)\b(\d+(?:\.\d{3})+(?:,\d+)?)\s?([°|A-Za-z]+[2|3]?)(?:\/([A-Za-z]+[2|3]?))?(?:\b|$)(\s?-?)",
        r"(?i)\b(\d+(?:,\d{3})+(?:\.\d+)?)\s?([°|A-Za-z]+[2|3]?)(?:\/(A-Za-z+[2|3]?))?(?:\b|$)(\s?-?)",
        r"(?i)\b(\d+(?:,\d+))\s?([°|A-Za-z]+[2|3]?)(?:\/(A-Za-z+[2|3]?))?(?:\b|$)(\s?-?)",
        r"(?i)\b(\d+(?:\.\d+)?)\s?([°|A-Za-z]+[2|3]?)(?:\/(A-Za-z+[2|3]?))?(?:\b|$)(\s?-?)",
    ]
    reg_meansure_2 = [
        r"(?i)(?:\b|^)(\d+(?:,\d+))\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)?(\s?-\s?)(\d+(?:,\d+))\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)",
        r"(?i)(?:\b|^)(\d+(?:\.\d{3})+(?:,\d+)?)\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)",
        r"(?i)(?:\b|^)(\d+(?:,\d{3})+(?:\.\d+)?)\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)",
        r"(?i)(?:\b|^)(\d+(?:,\d+))\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)",
        r"(?i)(?:\b|^)(\d+(?:\.\d+)?)\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)",
    ]
    for _reg in reg_meansure_1:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.groups()
            mtxt = f" {read_nnumber(_tmp[0], is_decimal=True)} "
            mtxt += f"{dict_base_unit[_tmp[1]] if _tmp[1] in dict_base_unit else _tmp[1]} {'trên' if '/' in match.group() else ''}"
            if _tmp[2] is not None: mtxt += f"{dict_base_unit[_tmp[2]] if _tmp[2] in dict_base_unit else _tmp[2]} "
            mtxt += f"{_tmp[3]} "
            text = text.replace(match.group(), mtxt)
    
    for _reg in reg_meansure_2:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.groups()
            if len(_tmp) == 5:
                # mtxt = f" {read_nnumber(_tmp[0], is_decimal=True)} đến {read_nnumber(_tmp[2], is_decimal=True)} {dict_currency_unit[_tmp[3]] if _tmp[3] in dict_currency_unit else _tmp[3]} {_tmp[4]}"
                mtxt = []
                for word in _tmp:
                    if word is not None and word[0].isdigit():
                        mtxt.append(read_nnumber(word, is_decimal=True))
                    elif word in dict_currency_unit:
                        mtxt.append(dict_currency_unit[word])
                    else:
                        mtxt.append(word)
                mtxt = " ".join([ch for ch in mtxt if ch is not None]).replace("-", "đến")
            else:
                mtxt = f" {read_nnumber(_tmp[0], is_decimal=True)} {dict_currency_unit[_tmp[1]] if _tmp[1] in dict_currency_unit else _tmp[1]} {_tmp[2]}"
            text = text.replace(match.group(), mtxt)

    reg_n_roman = [
        r"\b(thứ|lần|kỷ|kỉ|kì|kỳ|khoá|cấp|độ|đoạn)\s+([V|I|X]{1,5})\b"
    ]
    reg_n_phone = [
        r"([^(\w|\d|\.)]|^)((\+\d{1,3})|0)[-\s.]?\d{1,3}[-\s.]?\d{3}[-\s.]?\d{4}\b", 
        r"([^(\w|\d|\.)]|^)((\+\d{1,3})|0)[-\s.]?\d{2,3}[-\s.]?\d{2}[- .]?\d{2}[- .]?\d{2}\b",
        r"([^(\w|\d|\.)]|^)((\+\d{1,3})|0)[-\s.]?\d{1,3}[-\s.]?\d{1,2}[-\s.]?\d{2,3}[-\s.]?\d{3}\b",
        r"\b1[89]00[\s\.]?[\d\s\.]{4,8}\b",
    ]
    reg_n_from_to = [
        r"(?i)\b\d+(\.\d+)\s?(\-)\s?\d+(\.\d+)?",
        r"(?i)\b\d+(\,\d+)\s?(\-)\s?\d+(\,\d+)?",
        r"(?i)\b\d\s?(\-)\s?\d+",
    ]
    for _reg in reg_n_roman:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.groups()
            mtxt = f" {_tmp[0]} {read_nroman(_tmp[1].upper())} "
            text = text.replace(match.group(), mtxt)
    for _reg in reg_n_phone:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.group()
            mtxt = read_ndigit(_tmp)
            text = text.replace(match.group(), mtxt)

    for _reg in reg_n_from_to:
        for match in re.compile(_reg).finditer(text):
            _tmp = match.group().replace(" ", "")
            _sep = "/" if "/" in _tmp else "-"
            _tmp = _tmp.split(_sep)
            mtxt = f" {read_nnumber(_tmp[0], is_decimal=True)} {'đến' if _sep == '-' else 'trên'} {read_nnumber(_tmp[1], is_decimal=True)} "
            text = text.replace(match.group(), mtxt)
    return text
