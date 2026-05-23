import argparse
import time
import sys
import os

from password_cracker.attacks.dictionary import dictionary_attack
from password_cracker.attacks.brute_force import brute_force_attack


# =========================================================================
# CONFIGURACIÓN DE PANTALLA: Solución para la estabilidad de la consola
# Desactivamos el almacenamiento en caché (buffering) de la salida de texto
# Esto obliga a que los textos y barras de progreso se muestren en tiempo real, solucionando fallos visuales típicos cuando ejecutamos el programa en Windows
# =========================================================================
os.environ["PYTHONUNBUFFERED"] = "1"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True)

# Los algoritmos que se pueden utilizar
VALID_ALGORITHMS = [
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512"
]


# Esta función ayuda a procesar las posiciones que ya conocemos de la contraseña
# Si el usuario nos pasa una lista como ['0:A', '3:1'], la transforma en un diccionario de Python: {0: 'A', 3: '1'} para que el ataque pueda consultarlo rápido
def parse_known_positions(known_list):

    positions = {}

    if not known_list:
        return positions

    for item in known_list:

        try:
            # Separamos el texto por los dos puntos    "0:A" -> pos = "0", char = "A"
            pos, char = item.split(":")
            # Guardamos la posición convirtiéndola a número entero 
            positions[int(pos)] = char

        except ValueError:
            # Si el usuario escribe mal el formato ( "0-A" en vez de "0:A"), avisamos del error
            sys.stderr.write(f"Formato inválido en --known: {item}\n")
            return {}

    return positions


# Función principal que configura los argumentos y arranca la herramienta
def run():

    # Inicializamos el configurador de argumentos con una pequeña descripción del proyecto
    parser = argparse.ArgumentParser(
        description="Password Cracker (educational tool)"
    )

    # Definimos los parámetros obligatorios
    parser.add_argument("--hash", required=True)    # El hash que queremos romper
    parser.add_argument("--algo", required=True, choices=VALID_ALGORITHMS)  # El algoritmo (uno de la lista)
    parser.add_argument("--attack", required=True, choices=["dict", "brute"])   # El tipo de ataque

    # Parámetros opcionales dependiendo del ataque que elija el usuario
    parser.add_argument("--wordlist")   # Ruta del diccionario para el ataque por diccionario
    parser.add_argument("--mask")   # Máscara para el ataque fuerza bruta

    # Parámetros avanzados para recortar el rango de búsqueda en fuerza bruta
    parser.add_argument("--min-length", type=int)
    parser.add_argument("--max-length", type=int)

    # Parámetros para añadir restricciones extras (nargs="*" permite recibir múltiples textos)
    parser.add_argument("--must-contain", nargs="*")    # Letras obligatorias
    parser.add_argument("--known", nargs="*")   # Posiciones conocidas

    # Analizamos los argumentos introducidos por el usuario en la terminal
    args = parser.parse_args()

    start_time = time.time()    # Empezamos a contar el tiempo global de la sesión

    # =========================
    # ATAQUE DICCIONARIO
    # =========================
    if args.attack == "dict":
        
        # Si elige diccionario pero indica el archivo de palabras, da error
        if not args.wordlist:
            sys.stderr.write("Error: debes indicar --wordlist\n")
            return

        # Llamamos a nuestra función de ataque por diccionario pasándole los datos limpios
        result, attempts = dictionary_attack(
            args.hash,
            args.wordlist,
            args.algo
        )

    # =========================
    # ATAQUE BRUTE FORCE
    # =========================
    elif args.attack == "brute":

        # Si elige fuerza bruta pero no indica una máscara plantilla, da error
        if not args.mask:
            sys.stderr.write("Error: debes indicar --mask\n")
            return

        # Procesamos la lista de posiciones conocidas para darle el formato correcto
        known_positions = parse_known_positions(args.known)

        # Llamamos a nuestra función de fuerza bruta
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
    # FINAL FLUSH: Aseguramos que la pantalla pinte todo lo pendiente antes del cierre
    # =========================
    sys.stdout.flush()
    sys.stderr.flush()

    # Imprimimos el bloque de resumen final con los resultados
    sys.stderr.write("\n--- RESULTADO ---\n")

    if result:
        sys.stderr.write(f"Contraseña encontrada: {result}\n")
    else:
        sys.stderr.write("No encontrada\n")

    sys.stderr.write(f"Intentos: {attempts}\n")
    sys.stderr.write(f"Tiempo: {end_time - start_time:.2f} segundos\n")

# Si ejecutamos el script directamente desde la terminal, se lanza la función run()
if __name__ == "__main__":
    run()