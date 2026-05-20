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

    # =========================
    # PROGRESO POR BLOQUES
    # =========================

    update_every = max(total_words // 1000, 1)
    counter = 0

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:

            with tqdm(
                total=total_words,
                desc="Dictionary attack",
                unit="word",
                file=sys.stdout,     
                dynamic_ncols=True,
                mininterval=0,    
                maxinterval=0.05,
                ascii=True 
            ) as pbar:

                for word in file:

                    word = word.strip()
                    attempts += 1
                    counter += 1

                    # =========================
                    # UPDATE POR BLOQUES
                    # =========================
                    if counter % update_every == 0:
                        pbar.update(update_every)

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
                        tqdm.write(f"Speed: {speed:.2f} words/s")

                        return word, attempts

    except FileNotFoundError:
        print("Wordlist no encontrada")
        return None, attempts

    elapsed = time.time() - start_time

    tqdm.write("\n[FAIL]")
    tqdm.write(f"Attempts: {attempts}")
    tqdm.write(f"Time: {elapsed:.2f}s")

    return None, attempts