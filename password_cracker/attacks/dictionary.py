import time
import sys
from tqdm import tqdm

from password_cracker.utils.hashing import hash_text


def dictionary_attack(hash_target, wordlist_path, algorithm):

    attempts = 0
    start_time = time.time()

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            total_words = sum(1 for _ in f)
    except FileNotFoundError:
        print("Wordlist no encontrada")
        return None, attempts

    tqdm.write(f"\n[INFO] Total palabras: {total_words}\n")

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:

            with tqdm(
                total=total_words,
                desc="Dictionary attack",
                unit="word",
                file=sys.stderr,
                dynamic_ncols=True,
                mininterval=0,
                maxinterval=0.1
            ) as pbar:

                for word in file:

                    word = word.strip()
                    attempts += 1

                    if hash_text(word, algorithm) == hash_target:

                        elapsed = time.time() - start_time
                        speed = attempts / elapsed if elapsed > 0 else 0

                        tqdm.write("\n[FOUND]")
                        tqdm.write(f"Password: {word}")
                        tqdm.write(f"Attempts: {attempts}")
                        tqdm.write(f"Time: {elapsed:.2f}s")
                        tqdm.write(f"Speed: {speed:.2f} words/s")

                        return word, attempts

                    pbar.update(1)

    except FileNotFoundError:
        print("Wordlist no encontrada")
        return None, attempts

    elapsed = time.time() - start_time

    tqdm.write("\n[FAIL]")
    tqdm.write(f"Attempts: {attempts}")
    tqdm.write(f"Time: {elapsed:.2f}s")

    return None, attempts