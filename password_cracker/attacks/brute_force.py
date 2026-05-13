import itertools

from password_cracker.utils.hashing import hash_text
from password_cracker.utils.mask import parse_mask


def brute_force_attack(hash_target, mask, algorithm):

    attempts = 0

    charsets = parse_mask(mask)

    for combination in itertools.product(*charsets):

        word = ''.join(combination)

        attempts += 1

        if hash_text(word, algorithm) == hash_target:
            return word, attempts

    return None, attempts