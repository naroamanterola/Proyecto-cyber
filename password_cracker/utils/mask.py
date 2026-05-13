from password_cracker.utils.charset import (
    LOWERCASE,
    UPPERCASE,
    NUMBERS,
    SPECIAL,
    ALL
)

MASK_TOKENS = {
    "?l": LOWERCASE,
    "?u": UPPERCASE,
    "?d": NUMBERS,
    "?s": SPECIAL,
    "?a": ALL
}


def parse_mask(mask):

    charsets = []

    i = 0

    while i < len(mask):

        if mask[i] == "?" and i + 1 < len(mask):

            token = mask[i:i+2]

            if token in MASK_TOKENS:
                charsets.append(MASK_TOKENS[token])
                i += 2
                continue

        charsets.append(mask[i])

        i += 1

    return charsets