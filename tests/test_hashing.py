from password_cracker.utils.hashing import hash_text

def test_sha1():
    assert hash_text("hola", "sha1") == "f7ff9e8b7bb7c... (hash correcto)"