# Importamos los grupos de caracteres que creamos en charset.py
from password_cracker.utils.charset import (
    LOWERCASE,
    UPPERCASE,
    NUMBERS,
    SPECIAL,
    ALL
)

# Creamos un diccionario para asociar cada "código de máscara" con su abecedario real
MASK_TOKENS = {
    "?l": LOWERCASE,
    "?u": UPPERCASE,
    "?d": NUMBERS,
    "?s": SPECIAL,
    "?a": ALL
}

# Esta función recibe la máscara del usuario y devuelve una lista indicando qué caracteres permitidos van en cada posición de la contraseña
def parse_mask(mask):

    # Aquí guardaremos el resultado posición por posición
    charsets = []

    # Índice para recorrer la máscara letra a letra
    i = 0

    while i < len(mask):

        # Si encontramos un signo de interrogación y hay otro carácter detrás, significa que podríamos estar ante máscara
        if mask[i] == "?" and i + 1 < len(mask):

            # Cortamos los dos caracteres (signo de interrogación + la letra)
            token = mask[i:i+2]

            # Si ese código existe en nuestro diccionario de MASK_TOKENS
            if token in MASK_TOKENS:
                # Añadimos el abecedario correspondiente a esa posición
                charsets.append(MASK_TOKENS[token])
                # Saltamos 2 posiciones hacia adelante en el texto para buscar la siguiente máscara
                i += 2
                continue
        
        # Si no era un código especial (era una letra normal), esa posición solo puede ser esa letra fija. La añadimos tal cual
        charsets.append(mask[i])

        # Avanzamos a la siguiente letra de la máscara
        i += 1

    # Devolvemos la lista con las reglas para cada posición de la contraseña
    return charsets