# Password Cracker

Educational password cracking tool developed in Python.

This project was created for academic purposes in the field of cybersecurity and ethical hacking.  
It implements different password cracking techniques such as dictionary attacks and brute force attacks with masks and constraints.

---

## Features

- Dictionary attack
- Brute force attack
- Mask-based brute force
- Multiple hash algorithms:
  - MD5
  - SHA1
  - SHA224
  - SHA256
  - SHA384
  - SHA512
- Constraints support:
  - Known positions
  - Required characters
  - Variable password lengths
- Progress bars with `tqdm`
- Attack metrics:
  - Attempts
  - Execution time
  - Speed

---

## Project Structure

password_cracker/
│
├── attacks/
│   ├── brute_force.py
│   └── dictionary.py
│
├── utils/
│   ├── hashing.py
│   ├── mask.py
│   └── charset.py
│
├── cli.py
└── __init__.py