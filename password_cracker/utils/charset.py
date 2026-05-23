import string

# Guarda todas las letras minúsculas (de la 'a' a la 'z')
LOWERCASE = string.ascii_lowercase

# Guarda todas las letras mayúsculas (de la 'A' a la 'Z')
UPPERCASE = string.ascii_uppercase

# Combinamos las anteriores para tener un grupo con todas las letras posibles
LETTERS = LOWERCASE + UPPERCASE

# Guarda los dígitos del 0 al 9 en formato de texto
NUMBERS = string.digits

# Guarda todos los signos de puntuación y caracteres especiales
SPECIAL = string.punctuation

# Juntamos absolutamente todo en una sola variable para cuando el usuario quiera hacer un ataque completo con cualquier tipo de carácter
ALL = LETTERS + NUMBERS + SPECIAL