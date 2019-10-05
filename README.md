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

## Attack Design Approach
### Brute-Force Attack
My main concern with this problem was avoiding needing to re-compute the character combinations for the increasing 
length of characters.
In order to avoid this, I used a list named `last_combos` to keep track of the combinations from when they were computed
 for a length *n - 1* string where *n* represents the current length of the passwords being computed.
Each time *n* increases, I multiply `last_combos` by the number of characters that can be in a valid password
 (currently restricted to lowercase ASCII characters). I perform this multiplication so that each valid character can be
 applied to an individual combination in the list. As each combination is computed, the combination is hashed to check
 if it is equal to the desired hash.

For example, let's say our valid characters and `last_combos` are defined as follows:
* `valid_characters = ['a', 'b', 'c']`
* `last_combos = ['a', 'b', 'c'] (combinations from n = 1)`

In order to generate all possible combinations of `valid_characters` when *n = 2*, each character in `valid_characters`
is distributed to *y* elements in `last_combos`, where *y = (number of elements in `last_combos`)/
(number of valid characters)*. So, when distributing the elements of `valid_characters` in order,
`last_combos = ['aa', 'ba', 'ca', 'ab', 'bb', 'cb', 'ac', 'bc', 'cc']`.

As each valid character is distributed to `last_combos`, the MD5 hash of the new combination is computed and compared to
the desired hash so that computation time is not wasted on generating more combinations than necessary.
Finally, f the desired hash is never found, return `False`.

### Dictionary Attack
The implementation of this feature was trivial:
1. Open the dictionary file that was provided via the command line
1. Read in each line
1. Compare the hash of each line to the desired hash as they are read in.
1. Return `False` if the password was not found in the dictionary file.

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
