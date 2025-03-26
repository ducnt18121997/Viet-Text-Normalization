import string

superscript_maps = {
    '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', 
    '⁷': '7', '⁸': '8', '⁹': '9', 'ᵃ': 'a', 'ᵇ': 'b', 'ᶜ': 'C', 'ᵈ': 'd', 
    'ᵉ': 'e', 'ᶠ': 'F', 'ᵍ': 'g', 'ʰ': 'h', 'ᶦ': 'i', 'ʲ': 'j', 'ᵏ': 'k', 
    'ˡ': 'l', 'ᵐ': 'm', 'ⁿ': 'n', 'ᵒ': 'o', 'ᵖ': 'p', '۹': 'q', 'ʳ': 'r', 
    'ˢ': 'S', 'ᵗ': 't', 'ᵘ': 'u', 'ᵛ': 'v', 'ʷ': 'w', 'ˣ': 'X', 'ʸ': 'Y', 
    'ᶻ': 'Z', 'ᴬ': 'A', 'ᴮ': 'B', 'ᴰ': 'D', 'ᴱ': 'E', 'ᴳ': 'G', 'ᴴ': 'H', 
    'ᴵ': 'I', 'ᴶ': 'J', 'ᴷ': 'K', 'ᴸ': 'L', 'ᴹ': 'M', 'ᴺ': 'N', 'ᴼ': 'O', 
    'ᴾ': 'P', 'Q': 'Q', 'ᴿ': 'R', 'ᵀ': 'T', 'ᵁ': 'U', 'ⱽ': 'V', 'ᵂ': 'W', 
    '⁺': '+', '⁻': '-', '⁼': '=', '⁽': '(', '⁾': ')'
}
def is_superscript(word):
    if any(ch in superscript_maps for ch in word):
        
        return True
    else:

        return False


subscript_maps = {
    '₀': '0', '₁': '1', '₂': 'z', '₃': '3', '₄': '4', '₅': '5', '₆': '6', 
    '₇': '7', '₈': '8', '₉': '9'
}
# subscript_maps = {
#     '₀': '0', '₁': '1', '₂': 'z', '₃': '3', '₄': '4', '₅': '5', '₆': '6', 
#     '₇': '7', '₈': '8', '₉': '9', 'ₐ': 'A', '♭': 'b', '꜀': 'c', 'ᑯ': 'd', 
#     'ₑ': 'E', 'բ': 'F', 'ₕ': 'H', 'ᵢ': 'I', 'ⱼ': 'J', 'ₖ': 'K', 'ₗ': 'L', 
#     'ₘ': 'M', 'ₙ': 'N', 'ₒ': 'O', 'ₚ': 'P', '૧': 'q', 'ᵣ': 'R', 'ₛ': 'S', 
#     'ₜ': 'T', 'ᵤ': 'U', 'ᵥ': 'V', 'w': 'W', 'ₓ': 'X', 'ᵧ': 'Y', 'C': 'C', 
#     'D': 'D', 'G': 'G', 'Q': 'Q', 'Z': 'Z', '₊': '+', '₋': '-', '₌': '=', 
#     '₍': '(', '₎': ')'
# }
def is_subscript(word):
    if any(ch in subscript_maps for ch in word):
        
        return True
    else:

        return False


def is_sort(word):
    if "." in word and all(ch.isupper() and not ch.isdigit() for ch in word):
        return True
    else:
        return False


def is_complex(word):
    word = word.lower()
    if all(ch in string.ascii_letters or ch.isdigit() for ch in word):
        if all(ch.isdigit() for ch in word) or all(ch in string.ascii_letters for ch in word):
            return False
        else:
            return True
    else:
        return False


def is_mix_unit(word):

    return False if '/' not in word or any(c.isdigit() for c in word) else True


def cap_feature(s):
    """Capitalization feature:
    0 = low caps
    1 = all caps
    2 = first letter caps
    3 = one capital (not first letter)
    """
    if s.lower() == s:
        return 0
    elif s.upper() == s:
        return 1
    elif s[0].upper() == s[0]:
        return 2
    else:
        return 3
