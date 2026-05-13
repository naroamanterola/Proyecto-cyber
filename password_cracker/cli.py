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


def run():

    parser = argparse.ArgumentParser(
        description="Password Cracker (educational tool)"
    )

    # =========================
    # ARGUMENTOS PRINCIPALES
    # =========================

    parser.add_argument(
        "--hash",
        required=True,
        help="Hash objetivo a crackear"
    )

    parser.add_argument(
        "--algo",
        required=True,
        choices=VALID_ALGORITHMS,
        help="Algoritmo de hash (md5, sha1, sha256...)"
    )

    parser.add_argument(
        "--attack",
        required=True,
        choices=["dict", "brute"],
        help="Tipo de ataque: dict o brute"
    )

    # =========================
    # DICCIONARIO
    # =========================

    parser.add_argument(
        "--wordlist",
        help="Ruta del diccionario (obligatorio si attack=dict)"
    )

    # =========================
    # FUERZA BRUTA CON MÁSCARA
    # =========================

    parser.add_argument(
        "--mask",
        help="Máscara tipo ?u?l?l?d?d (obligatorio si attack=brute)"
    )

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

        result, attempts = brute_force_attack(
            args.hash,
            args.mask,
            args.algo
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