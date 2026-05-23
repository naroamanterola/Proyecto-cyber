import hashlib

# Esta función la creamos para centralizar la generación de hashes de todo el proyecto
# Le pasamos el texto limpio y el algoritmo que queremos usar 
def hash_text(text, algorithm):
    
    # Usamos .new() para que sea dinámico. Así, según lo que elija el usuario, el programa configura el algoritmo automáticamente sin tener que hacer un IF para cada uno
    h = hashlib.new(algorithm)
    
    # Pasamos el texto a bytes con .encode() porque las funciones hash no trabajan con letras directamente, necesitan datos binarios para hacer los cálculos
    h.update(text.encode())
    
    # Devolvemos el hash final convertido a texto hexadecimal
    # Hacemos esto porque es el formato estándar en el que se guardan los hashes y así podemos compararlo fácilmente con la contraseña que queremos descifrar.
    return h.hexdigest()