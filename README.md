# Password Cracker

Educational password cracking tool developed in Python.

This project was created for academic purposes in the field of cybersecurity and ethical hacking.  
It implements different password cracking techniques such as dictionary attacks and brute force attacks with masks and constraints.

---

## Features

- **Dictionary attack**: efficient wordlist-based cracking
- **Brute force attack**: sequential character generation
- **Mask-based brute force**: targeting specific patterns
- **Multiple hash algorithms**: support for MD5, SHA1, SHA224, SHA256, SHA384, and SHA512
- **Constraints support**:
  - Known positions (`--known`)
  - Required characters (`--must-contain`)
  - Variable password lengths (`--min-length`, `--max-length`)
- **Optimized UI**: progress bars with `tqdm` updated in batches for maximum execution speed
- **Attack metrics**: total attempts, execution time, and speed

---

## Project structure

password_cracker/

├── attacks/
│ ├── brute_force.py
│ └── dictionary.py
│
├── utils/
│ ├── hashing.py
│ ├── mask.py
│ └── charset.py
│
├── cli.py
└── init.py


---

## Installation & setup

1. Download or clone this repository to your local machine.  
2. Install the project in editable mode along with its dependencies from the project root by running in your terminal:

```pip install -e .```

*Note: this will read the pyproject.toml file and register the command in your Python environment.*

---

## Usage examples

The tool is executed from the terminal through the main CLI module:

### 1. Dictionary attack
To attempt to crack an MD5 hash using the dictionary included in the project:

```python -m password_cracker.cli --hash 5f4dcc3b5aa765d61d8327deb882cf99 --algo md5 --attack dict --wordlist wordlists/dictionary.txt```

### 2. Mask-based brute force
To crack an MD5 hash of a 5-letter lowercase word using character masks:

```python -m password_cracker.cli --hash 5d41402abc4b2a76b9719d911017c592 --algo md5 --attack brute --mask ?l?l?l?l?l```

### 3. Brute force with constraints
To crack a SHA-1 hash knowing that the password has 4 characters, starts with 'h', and must contain the letter 'l':

```python -m password_cracker.cli --hash 99800b85d3383e3a2fb45eb7d0066a4879a9dad0 --algo sha1 --attack brute --mask ?l?l?l?l --known 0:h --must-contain l```

---

## Running tests

We have implemented a set of automated unit tests to ensure the cryptographic correctness of the hash generator and the logic of the attack filters.

To run all project tests, make sure pytest is installed and run from the project root:

```pytest```