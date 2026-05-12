import time
from attacks.dictionary import dictionary_attack
from attacks.brute_force import brute_force_attack
from utils.charset import LOWERCASE, LETTERS, ALPHANUMERIC, ALL

def main():
    print("=== PASSWORD CRACKER ===")

    hash_target = input("Introduce el hash: ")
    algorithm = input("Algoritmo (md5/sha1/sha256): ")

    print("\nTipo de ataque:")
    print("1) Diccionario")
    print("2) Fuerza bruta")

    choice = input("> ")

    start_time = time.time()

    if choice == "1":
        wordlist = "wordlists/dictionary.txt"
        result, attempts = dictionary_attack(hash_target, wordlist, algorithm)

    elif choice == "2":
        print("\nCharset:")
        print("1) Solo minúsculas")
        print("2) Letras")
        print("3) Letras + números")
        print("4) Todo")

        charset_choice = input("> ")

        if charset_choice == "1":
            charset = LOWERCASE
        elif charset_choice == "2":
            charset = LETTERS
        elif charset_choice == "3":
            charset = ALPHANUMERIC
        else:
            charset = ALL

        max_length = int(input("Longitud máxima: "))
        result, attempts = brute_force_attack(hash_target, charset, max_length, algorithm)

    else:
        print("Opción inválida")
        return

    end_time = time.time()

    print("\n--- RESULTADO ---")

    if result:
        print(f"Contraseña encontrada: {result}")
    else:
        print("No encontrada")

    print(f"Intentos: {attempts}")
    print(f"Tiempo: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":
    main()