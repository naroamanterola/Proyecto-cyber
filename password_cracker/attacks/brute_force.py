import itertools
import time
import sys
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

    total = 0
    for length in range(min_length, max_length + 1):
        current_charsets = charsets[:length]
        total += len(list(itertools.product(*current_charsets)))

    tqdm.write(f"\n[INFO] Total combinaciones: {total}\n")

    # =========================
    # PROGRESO POR BLOQUES
    # =========================

    update_every = max(total // 1000, 1)  # ~1000 updates máximo
    counter = 0

    with tqdm(
        total=total,
        desc="Brute force",   
        unit="hash",
        file=sys.stdout,      
        dynamic_ncols=True,
        mininterval=0,        
        maxinterval=0.05,
        ascii=True 
    ) as pbar:

        for length in range(min_length, max_length + 1):

            current_charsets = charsets[:length]

            for combination in itertools.product(*current_charsets):

                word = ''.join(combination)

                counter += 1

                # =========================
                # UPDATE POR BLOQUES
                # =========================
                if counter % update_every == 0:
                    pbar.update(update_every)

                if not matches_constraints(
                    word,
                    must_contain,
                    known_positions
                ):
                    continue

                attempts += 1

                if hash_text(word, algorithm) == hash_target:

                    # flush progreso restante
                    remaining = counter % update_every
                    if remaining:
                        pbar.update(remaining)

                    elapsed = time.time() - start_time
                    speed = attempts / elapsed if elapsed > 0 else 0

                    tqdm.write("\n[FOUND]")
                    tqdm.write(f"Password: {word}")
                    tqdm.write(f"Attempts: {attempts}")
                    tqdm.write(f"Time: {elapsed:.2f}s")
                    tqdm.write(f"Speed: {speed:.2f} hashes/s")

                    return word, attempts

    elapsed = time.time() - start_time

    tqdm.write("\n[FAIL]")
    tqdm.write(f"Attempts: {attempts}")
    tqdm.write(f"Time: {elapsed:.2f}s")

    return None, attempts