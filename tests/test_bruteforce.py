from password_cracker.attacks.brute_force import brute_force_attack


# Basic test to verify that brute force with masks works correctly
def test_mask_basic():

    # md5("hello")
    hash_target = "5d41402abc4b2a76b9719d911017c592"

    # Run the attack using a mask of 5 lowercase letters (?l)
    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l?l",
        "md5"
    )

    # Verify that the brute force engine correctly cracks "hello"
    assert result == "hello"


# Test to verify that the engine respects required character constraints
def test_must_contain():

    # sha1("hola")
    hash_target = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"

    # Run the attack forcing candidate passwords to contain the letter "h"
    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l",
        "sha1",
        must_contain=["h"]
    )

    # Verify that the filter works and correctly finds "hola"
    assert result == "hola"


# Test to verify that the engine respects known fixed positions
def test_known_positions():

    # sha1("hola")
    hash_target = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"

    # Run the attack fixing the first character as "h"
    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l",
        "sha1",
        known_positions={0: "h"}
    )

    # Verify that the attack succeeds while respecting the fixed position rule
    assert result == "hola"


# Test to verify support for variable password lengths
def test_variable_length():

    # sha1("hola")
    hash_target = "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"

    # Tell the engine to try lengths between 4 and 6 characters
    result, attempts = brute_force_attack(
        hash_target,
        "?l?l?l?l?l?l",
        "sha1",
        min_length=4,
        max_length=6
    )

    # Verify that it finds "hola", proving that it can search shorter lengths than the full mask
    assert result == "hola"