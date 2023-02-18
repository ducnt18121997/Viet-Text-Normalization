"""config:
1: Cách đọc theo anh - mĩ (US)
2: Cách đọc theo anh - anh (UK)
3: Cách đọc theo thuần việt (vie)
"""
from .modules.en2vi import *


def en2vi(eng_string, domain=None):
    output_string = ""
    if domain in dict_domain_en_words.keys() and eng_string in dict_domain_en_words[domain]:
        output_string += dict_domain_en_words[domain][eng_string]
    elif eng_string in dict_en_words:
        output_string += dict_en_words[eng_string]
    else:
        try:
            output_string = reading_english(eng_string)
        except:
            print(f"\t** \033[91m Errors en2vi \033[0m               : {eng_string}")

    return output_string


# Thứ tự ưu tiên: lemmatize sang dạng vietlish -> api2vi -> cmu2vi
def reading_english(eng_string):
    output_string = word_lemmatize(eng_string)
    
    if output_string is None:
        output_string = ipa2vi(eng_string)
        
    if output_string is None:
        output_string = cmu2vi(eng_string)

    return output_string
