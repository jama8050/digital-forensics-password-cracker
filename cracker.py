import hashlib
import argparse

# A string of all printable ASCII characters
import time
from string import ascii_letters, digits, punctuation
# Dictionary used for brute forcing
b_dict = list(ascii_letters)
b_dict.extend(digits)
b_dict.extend(punctuation)
b_dict.extend([' ', '\t'])


# TODO: Implement multithreading?
# TODO: Implement GPU support?

# Needs two methods:
#   1. dictionary method
#   2. brute force method
# Dictionary will need to accept a wordlist txt file
# Brute force methodology will be.... interesting


# Reads the lines from the given file and returns list of all the lines
def read_wordlist(file_argument):
    with open(file_argument) as reader:
        lines = [x.strip("\n") for x in reader.readlines()]
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
    number_of_hashes = 0
    start_time = time.time()

    # For every word in the dictionary
    for word in used_dict:
        number_of_hashes += 1
        # Hash the word in the wordlist
        hashed_word = give_hash(word)

        # If found hash, return the word from the wordlist that worked
        if hashed_word == given_hash:
            return number_of_hashes,  (time.time() - start_time), word

    # If the password couldn't be found, return False
    return number_of_hashes, (time.time() - start_time), False


# Given the md5 hash, a dictionary to use (optional), and a limit on the length of the password, brute force the hash.
# Return:
#   False if no match found
#   password if match found
def brute_force(given_hash, used_dict=b_dict, limit=-1):
    last_combos = ['']

    i = 0
    # Infinite loop if no limit, else bounded by limit
    while (i < limit and limit != -1) or (limit == -1):
        i += 1

        # Combinations we've done so far
        current_combos = []

        # For every character in the provided dictionary
        for c in used_dict:

            # For every combination that was generated last iteration
            for combo in last_combos:
                # Generate and hash the current combination
                immediate_combo = c + combo
                current_hash = give_hash(immediate_combo)

                # print('Trying hash "{}"\t{}'.format(immediate_combo, current_hash))
                if current_hash == given_hash:
                    # Desired clear-text found, return it and the number of hashes we did before completion
                    return i, current_hash
                else:
                    # immediate_combo is not the desired clear-text, add it to the current_combos for the next iteration
                    current_combos.append(immediate_combo)

        # Loop completed, replace old "last_combos" with "current_combos" for next iteration
        last_combos = current_combos

    # Couldn't find the hash after "i" tries, return False
    return i, False


# Hash a given string
def give_hash(s):
    current_hash = hashlib.md5()
    current_hash.update(str.encode(s))
    return current_hash.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Python3 md5 cracker (default brute force)",
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

    # If given wordlist, use it
    if attack_type == "Dictionary":
        wordlist = read_wordlist(parsed.wordlist)
        number_of_hashes, elapsed, result = dict_attack(parsed.hash, wordlist)
    else:
        # Brute force mode
        number_of_hashes, result = brute_force(parsed.hash)

    if result is False:
        print(attack_type, "attack failed to find a match.")
    else:
        print("Match found: \"{}\"".format(result))


if __name__ == "__main__":
    main()
