from password_cracker.attacks.dictionary import dictionary_attack

# Test to verify that the dictionary attack works correctly
def test_dictionary():
    
    # password (md5)
    hash_target = "5f4dcc3b5aa765d61d8327deb882cf99"  

    # We launch the attack by passing the target hash, the path to our wordlist, and the algorithm
    result, attempts = dictionary_attack(
        hash_target,
        "wordlists/dictionary.txt",
        "md5"
    )

    # This assert checks that 'result' is NOT None
    # If it is not None, it means the program correctly read the file and found the password
    assert result is not None