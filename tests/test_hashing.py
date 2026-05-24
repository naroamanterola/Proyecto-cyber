from password_cracker.utils.hashing import hash_text

# Test to verify that the hashing attack works correctly
def test_sha1():
    # We directly check whether passing the word "hola" to the "sha1" algorithm
    # returns exactly the official SHA1 hash of that word
    assert hash_text("hola", "sha1") == "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"