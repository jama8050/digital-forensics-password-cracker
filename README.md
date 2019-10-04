# MD5PyCrack
Python 3 MD5 hash cracker restricted to passwords of length 1 - 5.

## Support Attack Methods
* Brute-force attack.
* Dictionary attacks.

## Limitations
Restricted to:
* Unsalted hashes,
* MD5,
* Passwords that are 1 - 5 characters long,
* And lowercase ASCII characters only.

## Usage
Enter the following command to see the usage information:
```python
python3 cracker.py -h
```

## Planned Features
1. Implement the [itertools](https://docs.python.org/3/library/itertools.html) library.
1. Multi-threading.
1. Implement known MD5 breaking techniques.
1. Implement mangling rules for dictionary attacks.
1. GPU support.
1. Support for other hashing algorithms (e.g., SHA-256, SHA-1).

## Prerequisites
This program was developed with Python 3.7
and I am unaware what the oldest version of Python is compatible with this script.

## Credit
Created by Jacob Malcy for CYBR-5830 Digital Forensics, Fall 2019, Project 1
