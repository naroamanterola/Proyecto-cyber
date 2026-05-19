from password_cracker.attacks.brute_force import brute_force_attack


def test_mask_basic():

    # md5("hello")
    hash_target = "5d41402abc4b2a76b9719d911017c592"

    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l?l",
        "md5"
    )

    assert result == "hello"


def test_must_contain():

    # sha1("hola")
    hash_target = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"

    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l",
        "sha1",
        must_contain=["h"]
    )

    assert result == "hola"


def test_known_positions():

    # sha1("hola")
    hash_target = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"

    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l",
        "sha1",
        known_positions={0: "h"}
    )

    assert result == "hola"


def test_variable_length():

    # sha1("hola")
    hash_target = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"

    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l?l?l",
        "sha1",
        min_length=4,
        max_length=6
    )

    assert result == "hola"