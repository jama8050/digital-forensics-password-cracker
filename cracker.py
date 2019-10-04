from hashlib import md5
from _md5 import md5
from argparse import ArgumentParser
from time import time

# A string of all printable ASCII characters, with some of the whitespace ones removed
from string import ascii_lowercase, printable

# TODO: Implement multithreading?
# TODO: Implement GPU support?


# Reads the lines from the given file and returns list of all the lines
def read_wordlist(file_argument):
    with open(file_argument, 'rb') as reader:
        lines = [line.strip() for line in reader.readlines() if len(line.strip()) > 0]
    return lines


# Given the md5 hash and a dictionary to use, brute force the hash.
# Return:
#   Number of hashes attempted
#   Number of seconds elapsed while cracking password
#   Hash result:
#       False if no match found
#       password if match found
def dict_attack(given_hash, used_dict):
    # Number of hashes computed in total
    n_tries = 0
    start_time = time()

    # For every word in the dictionary
    for word in used_dict:
        n_tries += 1

        # If found hash, return the word from the wordlist that worked
        if md5(word).hexdigest() == given_hash:
            return n_tries, (time() - start_time), word

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
        print("Brute-force cracking with passwords of {} length".format(brute_length))

        prior_size = len(last_combos)
        last_combos *= dict_len

        i = 0
        for c in used_dict:
            for j in range(0, prior_size):
                n_tries += 1
                last_combos[i] += c
                if md5(last_combos[i]).hexdigest() == given_hash:
                    return n_tries, (time() - start_time), last_combos[i]
                else:
                    i += 1

        # Im just going to keep this here. It's from a previous attempt that I forgot to commit
        # for i in range(0, lc_size):
        #     immediate_combo = last_combos[i]
        #     for c in used_dict:
        #         n_tries += 1
        #         sub_h = md5(immediate_combo + c).hexdigest()
        #         print((immediate_combo + c).decode("ascii"))
        #
        #         # print('Trying hash "{}"\t{}'.format(immediate_combo, current_hash))
        #         if sub_h == given_hash:
        #             # Desired clear-text found, return it and the number of hashes we did before completion
        #             return n_tries, (time() - start_time), (immediate_combo + c)
        #         else:
        #             # immediate_combo is not the desired clear-text, add it to the current_combos for the next iteration
        #             last_combos[i] += c
        #
        # # Loop completed, replace old "last_combos" with "current_combos" for next iteration
        # #last_combos = current_combos

    # Couldn't find the hash after "i" tries, return False
    return n_tries, (time() - start_time), False


if __name__ == "__main__":
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

    attack_type = "Dictionary" if parsed.wordlist else "Brute-force"
    hash_to_crack = parsed.hash

    # If given wordlist, use it
    if attack_type == "Dictionary":
        wordlist = read_wordlist(parsed.wordlist)
        number_of_hashes, elapsed, result = dict_attack(hash_to_crack,
                                                        wordlist)
    else:
        # Brute force mode
        # [b'a', b'b', b'c'],[c.encode(encoding) for c in printable[:-2]]
        number_of_hashes, elapsed, result = brute_force(hash_to_crack,
                                                        [c.encode(encoding) for c in ascii_lowercase])

    print("Attacked hash for {} seconds.".format(elapsed))
    print("Tried {} different passwords.".format(number_of_hashes))

    # If we didn't find a match, print as such
    if result is False:
        print(attack_type, "attack failed to find a match.")
    else:
        print('Match found: "{}"'.format(result.decode('ascii')))

