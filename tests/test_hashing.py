from password_cracker.utils.hashing import hash_text

# Test para validar que el ataque el hashing funciona correctamente
def test_sha1():
    # Comprobamos directamente si al pasarle la palabra "hola" al algoritmo "sha1", el resultado que nos devuelve coincide exactamente con el hash real oficial de esa palabra
    assert hash_text("hola", "sha1") == "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"