from hashlib import md5
from _md5 import md5
from argparse import ArgumentParser
from time import time

# A string of all printable ASCII characters, with some of the whitespace ones removed
from string import ascii_lowercase, printable

# TODO: Implement multithreading?
# TODO: Implement GPU support?


# Given the md5 hash and the name of the file to use as the dictionary,
# perform a dictionary attack against the given hash.
# Return:
#   Number of hashes attempted
#   Number of seconds elapsed while cracking password
#   Hash result:
#       False if no match found
#       password if match found
def dict_attack(given_hash, file_argument):
    # Number of hashes computed in total
    n_tries = 0
    start_time = time()

    # For every word in the dictionary
    with open(file_argument, 'rb') as reader:
        for word in reader:
            n_tries += 1

            # If found hash, return the word from the wordlist that worked
            if md5(word.strip()).hexdigest() == given_hash:
                return n_tries, (time() - start_time), word.strip()

    # If the password couldn't be found, return False
    return n_tries, (time() - start_time), False


# Given the md5 hash, a dictionary to use, and a limit on the length of the password (optional), brute force the hash.
# Return:
#   Number of hashes attempted
#   Number of seconds elapsed while cracking password
#   Hash result:
#       False if no match found
#       password if match found
def brute_force(given_hash, used_dict, limit=-1):
    # Number of valid characters given to us in the dictionary
    dict_len = len(used_dict)

    # How many hashes in total have been tried
    n_tries = 0

    # Current length of the hashes
    brute_length = 0

    # List of the hashes from the previous iteration of the while loop
    last_combos = [b'']

    # Time we start cracking
    start_time = time()

    # Infinite loop if no limit, else bounded by limit
    while (brute_length < limit and limit != -1) or (limit == -1):
        brute_length += 1
        print("Brute-force cracking with passwords of length {}".format(brute_length))

        # Size before we increase list size
        prior_size = len(last_combos)

        # ['a', 'b']*3 becomes ['a', 'b', 'a', 'b', 'a', 'b']
        last_combos *= dict_len

        # index in range [0, len(last_combos)] (inclusive)
        i = 0

        # For individual character in available characters list (used_dict)
        for c in used_dict:
            # Append character c to "prior_size" entries in the list
            for j in range(0, prior_size):
                # Increment number of attempted hashes
                n_tries += 1

                # Append character c to specific combination at index i
                last_combos[i] += c

                # if new combo, located at last_combos[i], hashes to desired value, return
                if md5(last_combos[i]).hexdigest() == given_hash:
                    return n_tries, (time() - start_time), last_combos[i]
                else:
                    # Move to next element in the last_combos list
                    i += 1

    # Couldn't find the hash after "i" tries, return False
    return n_tries, (time() - start_time), False


if __name__ == "__main__":
    # encoding we'll be using to encode characters with that will be hashed
    encoding = "ascii"
    parser = ArgumentParser(description="Python3 md5 cracker (default brute force)",
                                     epilog="Created by Jacob Malcy")

    # Add wordlist parameter, optional
    parser.add_argument("--wordlist",
                        help="Enable wordlist mode, providing a wordlist",
                        type=str)

    # Add md5 hash parameter
    parser.add_argument("hash",
                        help="The md5 hash to crack",
                        type=str)

    # Parse cmd arguments
    parsed = parser.parse_args()

    # Determine what type of attack we'll be performing
    attack_type = "Dictionary" if parsed.wordlist else "Brute-force"
    hash_to_crack = parsed.hash

    # If given wordlist, use it
    if attack_type == "Dictionary":
        number_of_hashes, elapsed, result = dict_attack(hash_to_crack,
                                                        parsed.wordlist)
    else:
        # Brute force mode
        number_of_hashes, elapsed, result = brute_force(hash_to_crack,
                                                        [c.encode(encoding) for c in ascii_lowercase])

    print("Attacked hash for {} seconds.".format(elapsed))
    print("Tried {} different passwords.".format(number_of_hashes))

    # If we didn't find a match, print as such
    if result is False:
        print(attack_type, "attack failed to find a match.")
    else:
        print('Match found: "{}"'.format(result.decode('ascii')))

