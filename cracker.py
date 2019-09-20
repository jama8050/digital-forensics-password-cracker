import hashlib
import argparse

# A string of all printable ASCII characters
from string import printable

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


# Given a list of words, hash each word against the given md5 hash
def dict_attack(arr, given_hash):
    for word in arr:
        # Hash the word in the wordlist
        h = hashlib.md5()
        h.update(str.encode(word))
        hashed_word = h.hexdigest()
        # print("Checking with \"{}\", \"{}\"".format(word, hashed_word))

        # If found hash, return the word from the wordlist that worked
        if hashed_word == given_hash:
            return word

    # If the password couldn't be found, return False
    return False


# Given the md5 hash, brute force the hash
def brute_force(given_hash):
    print("NO")


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

    # If given wordlist, use it
    if parsed.wordlist:
        wordlist = read_wordlist(parsed.wordlist)
        result = dict_attack(wordlist, parsed.hash)

        if result is False:
            print("Dictionary failed to find a match.")
        else:
            print("Match found: \"{}\"".format(result))
    else:
        # Brute force mode
        brute_force(parsed.hash)


if __name__ == "__main__":
    main()
