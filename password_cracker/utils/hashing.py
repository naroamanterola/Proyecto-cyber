import hashlib

def hash_text(text, algorithm):
    h = hashlib.new(algorithm)
    h.update(text.encode())
    return h.hexdigest()