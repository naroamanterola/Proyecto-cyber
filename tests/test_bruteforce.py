from password_cracker.attacks.brute_force import brute_force_attack

# Test básico para comprobar que la fuerza bruta con máscaras funciona
def test_mask_basic():

    # md5("hello")
    hash_target = "5d41402abc4b2a76b9719d911017c592"

    # Lanzamos el ataque indicando una máscara de 5 letras minúsculas (?l)
    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l?l",
        "md5"
    )

    # Verificamos que el motor de fuerza bruta descifre correctamente la palabra "hello"
    assert result == "hello"


# Test para verificar que el motor respeta el filtro de caracteres obligatorios
def test_must_contain():

    # sha1("hola")
    hash_target = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"

    # Lanzamos el ataque obligando a que la palabra candidata contenga sí o sí la letra "h"
    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l",
        "sha1",
        must_contain=["h"]
    )

    # Verificamos que el filtro funcione y encuentre "hola" correctamente
    assert result == "hola"


# Test para verificar que el motor respeta las posiciones fijas que ya conocemos
def test_known_positions():

    # sha1("hola")
    hash_target = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"

    # Lanzamos el ataque fijando que en la posición cero tiene que haber una "h"
    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l",
        "sha1",
        known_positions={0: "h"}
    )

    # Comprobamos que el ataque tiene éxito respetando esa regla de posición
    assert result == "hola"


# Test para comprobar que el programa maneja bien rangos de longitud variables
def test_variable_length():

    # sha1("hola")
    hash_target = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"

    # Le decimos al programa que pruebe longitudes desde 4 hasta 6 caracteres
    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l?l?l",
        "sha1",
        min_length=4,
        max_length=6
    )

    # Verificamos que encuentre "hola", demostrando que sabe buscar en longitudes más cortas que la máscara completa
    assert result == "hola"