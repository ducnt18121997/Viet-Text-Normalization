# Thư viện đọc NSWs dạng chữ sang tiếng việt
import unidecode
import unicodedata

from .config import *
from .modules.reading import *
from .modules.en2vi import *
from .en2vi import dict_en_chars, dict_en_common_words, en2vi


# Hàm xử lý đọc đường link và email
def URLE2words(urle_string: str) -> str:
    if urle_string.startswith(("https://", "https://")):
        urle_string = urle_string.split("//")[-1]
    if urle_string.endswith("/"): urle_string[:-1]
    urle_arr = urle_string.split(".")
    if len(urle_arr) == 2:
        output_string = " ".join([
            dict_website_name[urle_arr[0]] if urle_arr[0] in dict_website_name else en2vi(urle_arr[0]),
            "chấm",
            dict_website_domain[urle_arr[1]] if urle_arr[1] in dict_website_domain else en2vi(urle_arr[1])
        ])        
    else:
        output_string = "link đính kèm"

    return output_string


# Hàm xử lý từ viết hoa toàn bộ (dạng UPPER
def UPPER2words(upper_string: str, domain: str=None, ignore_en: bool=False) -> str:
    output_string = ""
    if len(upper_string) == 1:
        if upper_string in dict_vn_chars:
            output_string += dict_vn_chars[upper_string]
        elif unidecode.unidecode(upper_string) in dict_en_chars:
            output_string += dict_en_chars[unidecode.unidecode(upper_string)]
    elif domain is not None and domain in dict_abb_domain and upper_string in dict_abb_domain[domain]:
        output_string += dict_abb_domain[domain][upper_string]
    elif upper_string in dict_mono_abb:
        output_string += dict_mono_abb[upper_string]
    elif upper_string.lower() in dict_en_common_words:
        output_string += dict_en_common_words[upper_string.lower()]
    elif len(upper_string) <= 3:
        output_string += " ".join([dict_vn_chars[ch] for ch in upper_string if ch in dict_vn_chars])
    else:
        if upper_string.lower() in list_vn_words:
            output_string += upper_string.lower()
        elif len(upper_string) > 5:
            output_string += LOWER2words(upper_string.lower(), domain=domain, ignore_en=ignore_en)
        else:
            output_string += " ".join([dict_en_chars[ch] for ch in unidecode.unidecode(upper_string) if ch in dict_en_chars])

    return output_string


# Hàm xử lý từ viết thường toàn bộ (dạng lower)
def LOWER2words(lower_string: str, domain: str=None, ignore_en: bool=False) -> str:
    output_string = unicodedata.normalize('NFD', lower_string).encode('ascii', 'ignore').decode()
    if ignore_en is False:
        if lower_string in dict_en_words:
            output_string = dict_en_words[lower_string]
        else:
            output_string = en2vi(lower_string, domain=domain)

    return output_string


# Hàm xử lý ký tự số la mã
def ROMAN2words(roman_string: str) -> str:
    
    return NNUM2words(ROMAN2int(roman_string))
