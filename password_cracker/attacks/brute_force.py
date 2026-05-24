import itertools

from password_cracker.utils.hashing import hash_text
from password_cracker.utils.mask import parse_mask


def matches_constraints(word, must_contain=None, known_positions=None):

    # Required characters
    if must_contain:
        for char in must_contain:
            if char not in word:
                return False

    # Known positions
    if known_positions:
        for pos, char in known_positions.items():

            if pos >= len(word):
                return False

            if word[pos] != char:
                return False

    return True


def brute_force_attack(
    hash_target,
    mask,
    algorithm,
    min_length=None,
    max_length=None,
    must_contain=None,
    known_positions=None
):

    attempts = 0

    # Convert mask into character sets
    charsets = parse_mask(mask)

    # Default lengths
    if min_length is None:
        min_length = len(charsets)

    if max_length is None:
        max_length = len(charsets)

    # Try all possible lengths
    for length in range(min_length, max_length + 1):

        current_charsets = charsets[:length]

        # Generate all combinations
        for combination in itertools.product(*current_charsets):

            word = ''.join(combination)

            # Apply constraints
            if not matches_constraints(
                word,
                must_contain,
                known_positions
            ):
                continue

            attempts += 1

            # Compare hashes
            if hash_text(word, algorithm) == hash_target:

                return word, attempts

    return None, attempts