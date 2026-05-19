import time
from tqdm import tqdm

from password_cracker.utils.hashing import hash_text


def dictionary_attack(hash_target, wordlist_path, algorithm):

    attempts = 0
    start_time = time.time()

    # =========================
    # CONTAR TOTAL DE PALABRAS
    # =========================
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            total_words = sum(1 for _ in f)
    except FileNotFoundError:
        print("Wordlist no encontrada")
        return None, attempts

    print(f"\n[INFO] Total palabras: {total_words}\n")

    # =========================
    # ATAQUE CON PROGRESO
    # =========================
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:

            pbar = tqdm(total=total_words, desc="Dictionary attack", unit="word")

            for word in file:

                word = word.strip()
                attempts += 1

                if hash_text(word, algorithm) == hash_target:

                    elapsed = time.time() - start_time
                    speed = attempts / elapsed if elapsed > 0 else 0

                    pbar.close()

                    print("\n[FOUND]")
                    print(f"Password: {word}")
                    print(f"Attempts: {attempts}")
                    print(f"Time: {elapsed:.2f}s")
                    print(f"Speed: {speed:.2f} words/s")

                    return word, attempts

                pbar.update(1)

            pbar.close()

    except FileNotFoundError:
        print("Wordlist no encontrada")
        return None, attempts

    # =========================
    # NO ENCONTRADO
    # =========================
    elapsed = time.time() - start_time

    print("\n[FAIL]")
    print(f"Attempts: {attempts}")
    print(f"Time: {elapsed:.2f}s")

    return None, attempts