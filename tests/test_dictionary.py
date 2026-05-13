from password_cracker.attacks.dictionary import dictionary_attack

def test_dictionary():
    hash_target = "5f4dcc3b5aa765d61d8327deb882cf99"  # password (md5)

    result, attempts = dictionary_attack(
        hash_target,
        "wordlists/dictionary.txt",
        "md5"
    )

    assert result is not None