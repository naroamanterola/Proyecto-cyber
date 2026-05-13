from password_cracker.attacks.brute_force import brute_force_attack

def test_mask():
    hash_target = "5f4dcc3b5aa765d61d8327deb882cf99"

    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l?l?l",
        "md5"
    )

    assert result is not None