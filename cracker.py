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


def build_hash(l, translate_dict):
    return b''.join([translate_dict[val] for val in l])


# Given the md5 hash, a dictionary to use, and a limit on the length of the password (optional), brute force the hash.
# Return:
#   Number of hashes attempted
#   Number of seconds elapsed while cracking password
#   Hash result:
#       False if no match found
#       password if match found
def brute_force(given_hash, used_dict, limit=-1):
    dict_len = len(used_dict)
    # How many hashes in total have been tried
    n_tries = 0

    # Current length of the hashes
    brute_length = 0

    # array of indexes representing values in used_dict
    current_chars = []

    # Time we start cracking
    start_time = time()

    # Infinite loop if no limit, else bounded by limit
    while (brute_length < limit and limit != -1) or (limit == -1):
        brute_length += 1

        # Since increasing number of characters to brute force, add a new place to the array
        current_chars.append(0)

        print("Brute-force cracking with passwords of {} length".format(brute_length))

        done_full_cascade = False
        # Continue until first value is max
        while current_chars[0] != dict_len and done_full_cascade is False:
            n_tries += 1
            # print("current_chars = ", end="")
            # print(current_chars)

            # Translate list into string, check if solution found, return if so
            built_string = build_hash(current_chars, used_dict)
            if md5(built_string).hexdigest() == given_hash:
                return n_tries, (time() - start_time), built_string

            # Last value has been tried as max, reset to zero and go down the chain, resetting maxes to zero
            # and incrementing the value just after the last occurrence of the max
            if current_chars[-1] == dict_len - 1:
                i = brute_length - 1
                while current_chars[i] == dict_len - 1:
                    current_chars[i] = 0
                    done_full_cascade = (i == 0)
                    i -= 1

                # Removes errors that occur when a full cascade is performed (when all values reset to zero)
                if done_full_cascade is False:
                    # print("incrementing index", i)
                    current_chars[i] += 1
            else:
                current_chars[-1] += 1

    # Couldn't find the hash after "n_tries" tries, return False
    return n_tries, (time() - start_time), False


if __name__ == "__main__":
    encoding = "ascii"
    parser = ArgumentParser(description="Python3 md5 cracker (default brute force)",
                                     epilog="Created by Jacob Malcy")

    # Add wordlist parameter, optional
    parser.add_argument("--wordlist",
                        help="Enable wordlist mode, providing a wordlist",
                        type=str)

    # Add argument for debug which uses used_dict brute-force mode
    parser.add_argument("--debug",
                        help="Pass debug characters to brute-force mode. DO NOT USE UNLESS TESTING",
                        action="store_true")

    # Add argument for debug which uses used_dict brute-force mode
    parser.add_argument("--advanced",
                        help="Pass all printable ASCII characters to brute-force mode. Slower.",
                        action="store_true")

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
        if parsed.debug and parsed.advanced:
            raise Exception("Cannot use debug and advanced mode simultaneously!")
        elif parsed.debug:
            print("!!DEBUG MODE ENABLED!!")
            brute_chars = [b'a', b'b', b'c']
        elif parsed.advanced:
            print("!!ADVANCED MODE ENABLED!!")
            brute_chars = [c.encode(encoding) for c in printable[:-5]]
        else:
            print("Only using lowercase characters")
            brute_chars = [c.encode(encoding) for c in ascii_lowercase]

        number_of_hashes, elapsed, result = brute_force(hash_to_crack,
                                                        brute_chars)
        # RUNTIME ANALYSIS

    print("Attacked hash for {} seconds.".format(elapsed))
    print("Tried {} different passwords.".format(number_of_hashes))

    # If we didn't find a match, print as such
    if result is False:
        print(attack_type, "attack failed to find a match.")
    else:
        print('Match found: "{}"'.format(result.decode('ascii')))

