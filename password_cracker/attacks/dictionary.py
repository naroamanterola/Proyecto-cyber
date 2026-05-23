import time
import sys
from tqdm import tqdm

# Importamos la función que creamos en hashing.py para calcular los hashes
from password_cracker.utils.hashing import hash_text

# Esta función realiza el ataque por diccionario. Recibe el hash, la ruta del archivo de texto con palabras y el algoritmo criptográfico.
def dictionary_attack(hash_target, wordlist_path, algorithm):

    attempts = 0    # Contador de intentos realizados
    start_time = time.time()    # Guardamos la hora exacta de inicio para medir el rendimiento

    # Primero abrimos el archivo solo para contar cuántas palabras tiene
    # Necesitamos este número para configurar el total en la barra de progreso
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            total_words = sum(1 for _ in f)
    except FileNotFoundError:
        print("Wordlist no encontrada")
        return None, attempts

    tqdm.write(f"\n[INFO] Total palabras: {total_words}\n")

    # =========================
    # PROGRESO POR BLOQUES
    # =========================

    update_every = max(total_words // 1000, 1)
    counter = 0

    try:
        # Abrimos de nuevo el archivo para empezar a leer y procesar las palabras
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:
            
            # Configuramos la barra de progreso de tqdm en la terminal
            with tqdm(
                total=total_words,
                desc="Dictionary attack",
                unit="word",
                file=sys.stdout,     
                dynamic_ncols=True,
                mininterval=0,    
                maxinterval=0.05,
                ascii=True 
            ) as pbar:

                # Recorremos el diccionario línea por línea
                for word in file:
                    
                    # Limpiamos los espacios en blanco y los saltos de línea del final de la palabra
                    word = word.strip()
                    attempts += 1
                    counter += 1

                    # =========================
                    # UPDATE POR BLOQUES
                    # =========================
                    # Si el contador llega al tamaño de nuestro bloque, actualizamos la barra de progreso
                    if counter % update_every == 0:
                        pbar.update(update_every)

                    # Ciframos la palabra actual y comprobamos si su hash coincide con el objetivo
                    if hash_text(word, algorithm) == hash_target:

                        # Si la encontramos, forzamos a la barra a actualizarse con los intentos que quedaban sueltos en el bloque actual antes de terminar.
                        remaining = counter % update_every
                        if remaining:
                            pbar.update(remaining)

                        # Calculamos las métricas finales de rendimiento
                        elapsed = time.time() - start_time
                        speed = attempts / elapsed if elapsed > 0 else 0

                        # Mostramos los resultados detallados por pantalla
                        tqdm.write("\n[FOUND]")
                        tqdm.write(f"Password: {word}")
                        tqdm.write(f"Attempts: {attempts}")
                        tqdm.write(f"Time: {elapsed:.2f}s")
                        tqdm.write(f"Speed: {speed:.2f} words/s")

                        return word, attempts   # Devolvemos la contraseña y los intentos

    except FileNotFoundError:
        print("Wordlist no encontrada")
        return None, attempts

    # Si el bucle termina y no hemos encontrado nada, calculamos métricas de fracaso
    elapsed = time.time() - start_time

    tqdm.write("\n[FAIL]")
    tqdm.write(f"Attempts: {attempts}")
    tqdm.write(f"Time: {elapsed:.2f}s")

    return None, attempts