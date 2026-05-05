import hashlib

def hash_text(text, algorithm="md5"):
    h = hashlib.new(algorithm)
    h.update(text.encode())
    return h.hexdigest()