import argparse
import time
import sys
import os

from password_cracker.attacks.dictionary import dictionary_attack
from password_cracker.attacks.brute_force import brute_force_attack


# =========================================================================
# DISPLAY CONFIGURATION
# Disable output buffering for better console stability on Windows
# =========================================================================
os.environ["PYTHONUNBUFFERED"] = "1"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True)

# Supported hashing algorithms
VALID_ALGORITHMS = [
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512"
]


# Parse known positions from:
# ['0:A', '3:1']
# into:
# {0: 'A', 3: '1'}
def parse_known_positions(known_list):

    positions = {}

    if not known_list:
        return positions

    for item in known_list:

        try:
            pos, char = item.split(":")
            positions[int(pos)] = char

        except ValueError:
            sys.stderr.write(f"Invalid format in --known: {item}\n")
            return {}

    return positions


# Main CLI function
def run():

    parser = argparse.ArgumentParser(
        description="Educational Password Cracker Tool"
    )

    # Required arguments
    parser.add_argument("--hash", required=True)
    parser.add_argument(
        "--algo",
        required=True,
        choices=VALID_ALGORITHMS
    )

    parser.add_argument(
        "--attack",
        required=True,
        choices=["dict", "brute"]
    )

    # Dictionary attack
    parser.add_argument("--wordlist")

    # Brute force attack
    parser.add_argument("--mask")

    parser.add_argument("--min-length", type=int)
    parser.add_argument("--max-length", type=int)

    parser.add_argument("--must-contain", nargs="*")
    parser.add_argument("--known", nargs="*")

    args = parser.parse_args()

    start_time = time.time()

    # =========================
    # DICTIONARY ATTACK
    # =========================
    if args.attack == "dict":

        if not args.wordlist:
            sys.stderr.write("Error: you must provide --wordlist\n")
            return

        result, attempts = dictionary_attack(
            args.hash,
            args.wordlist,
            args.algo
        )

    # =========================
    # BRUTE FORCE ATTACK
    # =========================
    elif args.attack == "brute":

        if not args.mask:
            sys.stderr.write("Error: you must provide --mask\n")
            return

        known_positions = parse_known_positions(args.known)

        result, attempts = brute_force_attack(
            args.hash,
            args.mask,
            args.algo,
            min_length=args.min_length,
            max_length=args.max_length,
            must_contain=args.must_contain,
            known_positions=known_positions
        )

    else:
        sys.stderr.write("Invalid attack type\n")
        return

    end_time = time.time()

    elapsed = end_time - start_time
    speed = attempts / elapsed if elapsed > 0 else 0

    # Final flush
    sys.stdout.flush()
    sys.stderr.flush()

    # =========================
    # RESULTS
    # =========================
    print("\n========== RESULTS ==========")

    print(f"Target Hash   : {args.hash}")
    print(f"Algorithm     : {args.algo}")
    print(f"Attack Type   : {args.attack}")

    if args.attack == "dict":
        print(f"Wordlist      : {args.wordlist}")

    elif args.attack == "brute":

        print(f"Mask          : {args.mask}")

        if args.min_length:
            print(f"Min Length    : {args.min_length}")

        if args.max_length:
            print(f"Max Length    : {args.max_length}")

        if args.must_contain:
            print(f"Must Contain  : {args.must_contain}")

        if args.known:
            print(f"Known Chars   : {args.known}")

    print("--------------------------------")

    if result:
        print(f"Password Found: {result}")
    else:
        print("Password Not Found")

    print(f"Attempts      : {attempts}")
    print(f"Execution Time: {elapsed:.2f} seconds")
    print(f"Speed         : {speed:.2f} hashes/s")

    print("================================")


# Run directly from terminal
if __name__ == "__main__":
    run()