import itertools
from utils.hashing import hash_text

def brute_force_attack(hash_target, charset, max_length, algorithm="md5"):
    attempts = 0

    for length in range(1, max_length + 1):
        for combination in itertools.product(charset, repeat=length):
            word = ''.join(combination)
            attempts += 1

            if hash_text(word, algorithm) == hash_target:
                return word, attempts

    return None, attempts