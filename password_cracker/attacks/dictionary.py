import time

from password_cracker.utils.hashing import hash_text


# Dictionary attack function
# Receives:
# - target hash
# - path to the wordlist
# - hashing algorithm
def dictionary_attack(hash_target, wordlist_path, algorithm):

    # Counter for total attempts
    attempts = 0

    # Store start time for performance metrics
    start_time = time.time()

    try:
        # Open the wordlist file
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:

            # Read file line by line
            for word in file:

                # Remove spaces and line breaks
                word = word.strip()

                attempts += 1

                # Generate hash and compare with target hash
                if hash_text(word, algorithm) == hash_target:

                    # Return password and attempts if found
                    return word, attempts

    except FileNotFoundError:

        # Error if wordlist does not exist
        print("Wordlist not found")

        return None, attempts

    # Return failure if password was not found
    return None, attempts