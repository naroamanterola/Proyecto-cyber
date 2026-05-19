import argparse
import time

from password_cracker.attacks.dictionary import dictionary_attack
from password_cracker.attacks.brute_force import brute_force_attack

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
            print(f"Formato inválido en --known: {item}")
            exit()

    return positions


def run():

    parser = argparse.ArgumentParser(
        description="Password Cracker (educational tool)"
    )

    # =========================
    # ARGUMENTOS PRINCIPALES
    # =========================

    parser.add_argument("--hash", required=True)
    parser.add_argument("--algo", required=True, choices=VALID_ALGORITHMS)
    parser.add_argument("--attack", required=True, choices=["dict", "brute"])

    # =========================
    # DICCIONARIO
    # =========================

    parser.add_argument("--wordlist")

    # =========================
    # BRUTE FORCE
    # =========================

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
            print("Error: debes indicar --wordlist")
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
            print("Error: debes indicar --mask")
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
        print("Ataque no válido")
        return

    end_time = time.time()

    # =========================
    # RESULTADO
    # =========================

    print("\n--- RESULTADO ---")

    if result:
        print(f"Contraseña encontrada: {result}")
    else:
        print("No encontrada")

    print(f"Intentos: {attempts}")
    print(f"Tiempo: {end_time - start_time:.2f} segundos")