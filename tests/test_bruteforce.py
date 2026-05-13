from password_cracker.attacks.brute_force import brute_force_attack

def test_mask():

    hash_target = "5d41402abc4b2a76b9719d911017c592"  # "hello"

    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l?l",
        "md5"
    )

    assert result == "hello"