import itertools
import time
from tqdm import tqdm

from password_cracker.utils.hashing import hash_text
from password_cracker.utils.mask import parse_mask


def matches_constraints(word, must_contain=None, known_positions=None):

    if must_contain:
        for char in must_contain:
            if char not in word:
                return False

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
    start_time = time.time()

    charsets = parse_mask(mask)

    if min_length is None:
        min_length = len(charsets)

    if max_length is None:
        max_length = len(charsets)

    # =========================
    # CALCULAR TOTAL DE COMBINACIONES (para tqdm)
    # =========================
    total = 0

    for length in range(min_length, max_length + 1):
        current_charsets = charsets[:length]
        total += len(list(itertools.product(*current_charsets)))

    print(f"\n[INFO] Total combinaciones: {total}\n")

    # =========================
    # BARRA DE PROGRESO
    # =========================
    pbar = tqdm(total=total, desc="Brute force", unit="hash")

    for length in range(min_length, max_length + 1):

        current_charsets = charsets[:length]

        for combination in itertools.product(*current_charsets):

            word = ''.join(combination)

            if not matches_constraints(
                word,
                must_contain,
                known_positions
            ):
                continue

            attempts += 1

            if hash_text(word, algorithm) == hash_target:

                elapsed = time.time() - start_time
                speed = attempts / elapsed if elapsed > 0 else 0

                pbar.close()

                print("\n[FOUND]")
                print(f"Password: {word}")
                print(f"Attempts: {attempts}")
                print(f"Time: {elapsed:.2f}s")
                print(f"Speed: {speed:.2f} hashes/s")

                return word, attempts

            pbar.update(1)

    pbar.close()

    elapsed = time.time() - start_time

    print("\n[FAIL]")
    print(f"Attempts: {attempts}")
    print(f"Time: {elapsed:.2f}s")

    return None, attempts