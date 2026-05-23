# Password Cracker

Educational password cracking tool developed in Python.

This project was created for academic purposes in the field of cybersecurity and ethical hacking.  
It implements different password cracking techniques such as dictionary attacks and brute force attacks with masks and constraints.

---

## Features

- **Dictionary attack**: efficient wordlist-based cracking
- **Brute force attack**: sequential character generation
- **Mask-based brute force**: target specific patterns 
- **Multiple hash algorithms**: support for MD5, SHA1, SHA224, SHA256, SHA384 and SHA512
- **Constraints support**:
  - Known positions (`--known`)
  - Required characters (`--must-contain`)
  - Variable password lengths (`--min-length`, `--max-length`)
- **Optimized UI**: progress bars with `tqdm` updated in blocks for maximum execution speed
- **Attack metrics**: total attempts, execution time and speed 

---

## Project structure

```
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
```


## Installation & setup

1. Descarga o clona este repositorio en tu equipo.
2. Instala el proyecto en modo editable junto con sus dependencias desde la raíz del proyecto ejecutando en tu terminal:

```pip install -e .```

*Nota: esto leerá el archivo pyproject.toml y registrará el comando en tu entorno de Python.*

---

## Usage examples

La herramienta se ejecuta desde la terminal a través del módulo principal de la interfaz:

### 1. Ataque por diccionario
Para intentar romper un hash MD5 utilizando el diccionario incluido en el proyecto:

```python -m password_cracker.cli --hash 5f4dcc3b5aa765d61d8327deb882cf99 --algo md5 --attack dict --wordlist wordlists/dictionary.txt```

### 2. Fuerza bruta con máscara
Para romper un hash MD5 de una palabra de 5 letras minúsculas (hello) usando máscaras de caracteres:

```python -m password_cracker.cli --hash 5d41402abc4b2a76b9719d911017c592 --algo md5 --attack brute --mask ?l?l?l?l?l```

### 3. Fuerza bruta con restricciones
Para romper un hash SHA-1 sabiendo que la contraseña tiene 4 caracteres, empieza por 'h' y contiene obligatoriamente la letra 'l':

```python -m password_cracker.cli --hash 99800b85d3383e3a2fb45eb7d0066a4879a9dad0 --algo sha1 --attack brute --mask ?l?l?l?l --known 0:h --must-contain l```

---

## Running tests

Hemos implementado un conjunto de pruebas unitarias automatizadas para asegurar la precisión criptográfica del generador de hashes y la lógica de los filtros de ataque.

Para ejecutar todos los tests del proyecto, asegúrate de tener pytest instalado y ejecuta en la raíz de la carpeta:

```pytest```
