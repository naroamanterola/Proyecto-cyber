import itertools
import time
import sys
import os
from tqdm import tqdm

# Importamos las herramientas que creamos para calcular hashes y entender máscaras
from password_cracker.utils.hashing import hash_text
from password_cracker.utils.mask import parse_mask

# Esta función la creamos para validar si una contraseña candidata cumple con las restricciones extras (letras obligatorias o posiciones que ya conocemos)
def matches_constraints(word, must_contain=None, known_positions=None):

    # Si hay caracteres obligatorios, revisamos que estén todos dentro de la palabra
    # Si falta uno solo, descartamos la palabra devolviendo False
    if must_contain:
        for char in must_contain:
            if char not in word:
                return False

    # Si conocemos posiciones fijas, lo comprobamos
    if known_positions:
        for pos, char in known_positions.items():
            # Si la palabra es más corta que la posición que buscamos, no es válida
            if pos >= len(word):
                return False
            # Si el carácter en esa posición no coincide con el que conocemos, se descarta
            if word[pos] != char:
                return False
            
    # Si pasa todos los filtros, la palabra es válida para ser atacada
    return True


# Esta es la función principal del ataque por fuerza bruta basado en máscaras
def brute_force_attack(
    hash_target,
    mask,
    algorithm,
    min_length=None,
    max_length=None,
    must_contain=None,
    known_positions=None
):

    # =========================
    # FIX GLOBAL WINDOWS BUFFERING
    # =========================
    # Forzamos a Python a no guardar en caché las salidas de pantalla en Windows
    # Esto evita retrasos raros al mostrar la barra de progreso
    os.environ["PYTHONUNBUFFERED"] = "1"

    attempts = 0    # Contador de intentos reales de hash
    start_time = time.time()    # Guardamos la hora de inicio

    # Traducimos la máscara del usuario a listas de caracteres
    charsets = parse_mask(mask)

    # Si el usuario no define longitudes, por defecto usamos el tamaño de la máscara
    if min_length is None:
        min_length = len(charsets)

    if max_length is None:
        max_length = len(charsets)

    # Calculamos de antemano el total de combinaciones posibles para la barra de progreso
    total = 0
    for length in range(min_length, max_length + 1):
        current_charsets = charsets[:length]
        total += len(list(itertools.product(*current_charsets)))

    tqdm.write(f"\n[INFO] Total combinaciones: {total}\n")

    # Optimizamos la barra actualizándola por bloques
    update_every = max(total // 1000, 1)
    counter = 0

    # Inicializamos la barra de progreso
    with tqdm(
        total=total,
        desc="Brute force",
        unit="hash",
        file=sys.stderr,      # Usamos stderr para evitar parpadeos y bugs visuales en la consola
        dynamic_ncols=True,
        mininterval=0,
        maxinterval=0,
        ascii=True,
        disable=False
    ) as pbar:

        # Bucle para probar diferentes longitudes si el usuario introduce min y max
        for length in range(min_length, max_length + 1):

            # Cortamos las listas de caracteres hasta la longitud actual
            current_charsets = charsets[:length]

            # Genera todas las combinaciones posibles combinando los conjuntos de caracteres
            for combination in itertools.product(*current_charsets):

                # Como combination es una tupla, las juntamos en un string    ('a', 'b', '1') --> "ab1" 
                word = ''.join(combination)

                counter += 1

                # =========================
                # UPDATE POR BLOQUES
                # =========================
                if counter % update_every == 0:
                    pbar.update(update_every)
                    sys.stderr.flush()
                    sys.stdout.flush()

                # Comprobamos si la palabra cumple con los filtros obligatorios
                # Si no los cumple, hacemos un 'continue' para saltárnosla e ir a la siguiente, ahorrándonos calcular el hash de una palabra que sabemos que es incorrecta
                if not matches_constraints(
                    word,
                    must_contain,
                    known_positions
                ):
                    continue
                
                # Si cumple los filtros, cuenta como un intento real y calculamos su hash
                attempts += 1

                # Comparamos el hash generado con nuestro objetivo
                if hash_text(word, algorithm) == hash_target:

                    # Forzamos la última actualización de la barra de progreso
                    remaining = counter % update_every
                    if remaining:
                        pbar.update(remaining)

                    sys.stderr.flush()
                    sys.stdout.flush()

                    # Calculamos el tiempo total transcurrido y la velocidad del ataque
                    elapsed = time.time() - start_time
                    speed = attempts / elapsed if elapsed > 0 else 0

                    tqdm.write("\n[FOUND]")
                    tqdm.write(f"Password: {word}")
                    tqdm.write(f"Attempts: {attempts}")
                    tqdm.write(f"Time: {elapsed:.2f}s")
                    tqdm.write(f"Speed: {speed:.2f} hashes/s")

                    return word, attempts

    elapsed = time.time() - start_time

    tqdm.write("\n[FAIL]")
    tqdm.write(f"Attempts: {attempts}")
    tqdm.write(f"Time: {elapsed:.2f}s")

    return None, attempts