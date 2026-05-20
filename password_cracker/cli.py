import argparse
import time
import sys
import os

from password_cracker.attacks.dictionary import dictionary_attack
from password_cracker.attacks.brute_force import brute_force_attack



os.environ["PYTHONUNBUFFERED"] = "1"

VALID_ALGORITHMS = [
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512"
]


def parse_known_positions(known_list):

    positions = {}

    if not known_list:
        return positions

    for item in known_list:

        try:
            pos, char = item.split(":")
            positions[int(pos)] = char

        except ValueError:
            sys.stderr.write(f"Formato inválido en --known: {item}\n")
            return {}   # 👈 mejor que exit()

    return positions


def run():

    parser = argparse.ArgumentParser(
        description="Password Cracker (educational tool)"
    )

    parser.add_argument("--hash", required=True)
    parser.add_argument("--algo", required=True, choices=VALID_ALGORITHMS)
    parser.add_argument("--attack", required=True, choices=["dict", "brute"])

    parser.add_argument("--wordlist")
    parser.add_argument("--mask")

    parser.add_argument("--min-length", type=int)
    parser.add_argument("--max-length", type=int)

    parser.add_argument("--must-contain", nargs="*")
    parser.add_argument("--known", nargs="*")

    args = parser.parse_args()

    start_time = time.time()

    # =========================
    # ATAQUE DICCIONARIO
    # =========================
    if args.attack == "dict":

        if not args.wordlist:
            sys.stderr.write("Error: debes indicar --wordlist\n")
            return

        result, attempts = dictionary_attack(
            args.hash,
            args.wordlist,
            args.algo
        )

    # =========================
    # ATAQUE BRUTE FORCE
    # =========================
    elif args.attack == "brute":

        if not args.mask:
            sys.stderr.write("Error: debes indicar --mask\n")
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
        sys.stderr.write("Ataque no válido\n")
        return

    end_time = time.time()

    # =========================
    # RESULTADO FINAL
    # =========================

    # 👇 IMPORTANTE: flush antes de cerrar CLI (Windows fix)
    sys.stdout.flush()
    sys.stderr.flush()

    sys.stderr.write("\n--- RESULTADO ---\n")

    if result:
        sys.stderr.write(f"Contraseña encontrada: {result}\n")
    else:
        sys.stderr.write("No encontrada\n")

    sys.stderr.write(f"Intentos: {attempts}\n")
    sys.stderr.write(f"Tiempo: {end_time - start_time:.2f} segundos\n")


if __name__ == "__main__":
    run()