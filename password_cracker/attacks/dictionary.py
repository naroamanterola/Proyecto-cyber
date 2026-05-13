from password_cracker.utils.hashing import hash_text

def dictionary_attack(hash_target, wordlist_path, algorithm):
    attempts = 0

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:
            for word in file:
                word = word.strip()
                attempts += 1

                if hash_text(word, algorithm) == hash_target:
                    return word, attempts

    except FileNotFoundError:
        print("Wordlist no encontrada")
        return None, attempts

    return None, attempts