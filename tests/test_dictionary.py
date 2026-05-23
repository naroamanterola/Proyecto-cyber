from password_cracker.attacks.dictionary import dictionary_attack

# Test para validar que el ataque por diccionario funciona correctamente
def test_dictionary():
    
    # password (md5)
    hash_target = "5f4dcc3b5aa765d61d8327deb882cf99"  

    # Lanzamos el ataque pasándole el hash objetivo, la ruta de nuestra wordlist y el algoritmo
    result, attempts = dictionary_attack(
        hash_target,
        "wordlists/dictionary.txt",
        "md5"
    )

    # Con este assert comprobamos que 'result' NO sea None 
    # Si es distinto de None, significa que el programa ha leido bien el archivo y ha encontrado la contraseña
    assert result is not None