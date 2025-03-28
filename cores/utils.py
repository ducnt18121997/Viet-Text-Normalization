import string
from typing import Dict

# Map of superscript characters to their normal equivalents
superscript_maps: Dict[str, str] = {
    "⁰": "0",
    "¹": "1",
    "²": "2",
    "³": "3",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
    "ᵃ": "a",
    "ᵇ": "b",
    "ᶜ": "C",
    "ᵈ": "d",
    "ᵉ": "e",
    "ᶠ": "F",
    "ᵍ": "g",
    "ʰ": "h",
    "ᶦ": "i",
    "ʲ": "j",
    "ᵏ": "k",
    "ˡ": "l",
    "ᵐ": "m",
    "ⁿ": "n",
    "ᵒ": "o",
    "ᵖ": "p",
    "۹": "q",
    "ʳ": "r",
    "ˢ": "S",
    "ᵗ": "t",
    "ᵘ": "u",
    "ᵛ": "v",
    "ʷ": "w",
    "ˣ": "X",
    "ʸ": "Y",
    "ᶻ": "Z",
    "ᴬ": "A",
    "ᴮ": "B",
    "ᴰ": "D",
    "ᴱ": "E",
    "ᴳ": "G",
    "ᴴ": "H",
    "ᴵ": "I",
    "ᴶ": "J",
    "ᴷ": "K",
    "ᴸ": "L",
    "ᴹ": "M",
    "ᴺ": "N",
    "ᴼ": "O",
    "ᴾ": "P",
    "Q": "Q",
    "ᴿ": "R",
    "ᵀ": "T",
    "ᵁ": "U",
    "ⱽ": "V",
    "ᵂ": "W",
    "⁺": "+",
    "⁻": "-",
    "⁼": "=",
    "⁽": "(",
    "⁾": ")",
}


def is_superscript(word: str) -> bool:
    """Check if word contains any superscript characters"""
    return any(ch in superscript_maps for ch in word)


# Map of subscript characters to their normal equivalents
subscript_maps: Dict[str, str] = {
    "₀": "0",
    "₁": "1",
    "₂": "z",
    "₃": "3",
    "₄": "4",
    "₅": "5",
    "₆": "6",
    "₇": "7",
    "₈": "8",
    "₉": "9",
}


def is_subscript(word: str) -> bool:
    """Check if word contains any subscript characters"""
    return any(ch in subscript_maps for ch in word)


def is_sort(word: str) -> bool:
    """Check if word is an uppercase abbreviation with periods"""
    return "." in word and all(ch.isupper() and not ch.isdigit() for ch in word)


def is_complex(word: str) -> bool:
    """Check if word contains a mix of letters and numbers"""
    word = word.lower()
    has_letter = any(ch in string.ascii_letters for ch in word)
    has_digit = any(ch.isdigit() for ch in word)
    return (
        has_letter
        and has_digit
        and all(ch in string.ascii_letters or ch.isdigit() for ch in word)
    )


def is_mix_unit(word: str) -> bool:
    """Check if word is a unit with slash but no numbers"""
    return "/" in word and not any(c.isdigit() for c in word)


def cap_feature(s: str) -> int:
    """
    Get capitalization feature:
    0 = lowercase
    1 = all caps
    2 = first letter caps
    3 = one capital (not first letter)
    """
    if s.lower() == s:
        return 0
    if s.upper() == s:
        return 1
    if s[0].upper() == s[0]:
        return 2
    return 3
