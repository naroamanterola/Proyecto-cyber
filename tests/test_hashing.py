from password_cracker.utils.hashing import hash_text

def test_sha1():
    assert hash_text("hola", "sha1") == "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"