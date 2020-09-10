# Jadon Schuler
# CSCE 557
# Copyright 2020

"""This module focuses on cracking the substitution cipher.

This program is meant to be executed from the command line using python 3. The
second argument should be the filename to decrypt,
e.g. 'python3 solvecipher.py [the_file]'

This program is mostly an automated tool for cracking the substitution cipher,
allowing the user to input cribbing, then looping over permutations to find the
correct one. NOTE: EVERY enciphered word MUST either be a dictionary word or
prepended with a star ('*'), or the program will not function.
"""

import sys
import string
import fileio as fio

SHORT_WORD_CUTOFF = 5

alphabet_chars = list(string.ascii_lowercase)
for i in range(10):
    alphabet_chars.append(str(i))

valid_chars = []
short_words = []
long_words = []
cribbing = []
plaintext_words = []
cipher_words = []
frequency = []

def decrypt(filename):
    """Preprocesses data and runs user I/O for the print file

    Args:
        filename: the name of the .txt file containing the cipher text.
    """
    # Reads and processes the cipher text
    cipher_text = fio.read_file_data(filename)
    words = cipher_text.split()
    for word in words:
        cipher_words.append(word)

    # Sets up dictionary subsets
    dictionary_words = fio.get_dictionary_words()
    for word in dictionary_words:
        if len(word) < SHORT_WORD_CUTOFF:
            short_words.append(word)
        else:
            long_words.append(word)

    # Counts and displays letter frequency for cribbing
    count_letter_frequency(cipher_text)
    print(frequency)

    cribbing_input()
    plaintext = decrypt_text()
    filename = input("Enter the (.txt) file you would like to write to: ")
    fio.write_to_file(filename, plaintext)

def count_letter_frequency(cipher_text):
    """Counts and returns the letter frequencies.

    Args:
        cipher_text: The cipher text to be analyzed.
    """
    letter_frequency = {}
    for character in cipher_text:
        if character not in (' ', '\n', '*'):
            if character not in letter_frequency:
                letter_frequency[character] = 1
            else:
                letter_frequency[character] += 1

    for character in letter_frequency:
        frequency.append([character, letter_frequency[character]])
    frequency.sort(reverse = True, key = lambda count: count[1])
    for item in frequency:
        valid_chars.append(item[0])

def cribbing_input():
    """Handles user cribbing input
    """
    print("For cribbing, please enter pairs of letters separated by spaces.")
    print("For example, \'qt xe\' would mean \'q\' becomes \'t\' and \'x\' becomes \'e\'.")
    cribbed_letters =  input("Enter cribbing: ").split()
    for pair in cribbed_letters:
        if len(pair) != 2:
            print("Invalid cribbing.")
            print("Continuing.....")
            return
        cribbing.append([pair[0], pair[1]])

def decrypt_text():
    """Deciphers the ciphertext.

    Returns:
        The plaintext recovered from the cipher text
    """
    # For storing the order of letters to be checked
    selected_chars = list()

    # Initializes the decryption table
    cipher_table = {}
    for character in valid_chars:
        cipher_table[character] = "".join(alphabet_chars)

    # Adds cribbed letters to the decryption table
    for pair in cribbing:
        if pair[0] in valid_chars:
            cipher_table[pair[0]] = pair[1]
            selected_chars.append(pair[0])
            valid_chars.remove(pair[0])

    # Initial result given cribbing
    update_table(cipher_table)
    print_progress(cipher_table)

    while len(valid_chars) > 0:
        next_char = valid_chars[0]
        # next_char = input("Choose next char to decrypt: ")
        # while next_char == "" or next_char[0] not in valid_chars:
        #     next_char = input("Invalid, try again: ")
        print("Decrypting " + next_char)
        valid_chars.remove(next_char)
        selected_chars.append(next_char)
        permutation_loop(selected_chars, cipher_table)
        update_table(cipher_table)
        print_progress(cipher_table)

    print(cipher_table)

    plaintext = get_plaintext(cipher_table)

    print("\n\n\nDecrytped text: " + plaintext)
    return plaintext

def permutation_loop(selected_chars, cipher_table):
    """Runs through the permutations of the selected characters.

    Args:
        selected_chars: the list of chars currently being deciphered

        cipher_table: the dictionary containing possible options for each letter
    """
    for curr_char in selected_chars:
        if len(cipher_table[curr_char]) > 1:
            for char in cipher_table[curr_char]:
                if get_error_status(selected_chars, cipher_table, curr_char, char):
                    print("Error found with " + curr_char + " as " + char + ".")
                    print("Deleting " + char + "...")
                    cipher_table[curr_char] = cipher_table[curr_char].replace(char, "")
                if len(cipher_table[curr_char]) == 0:
                    cipher_table[curr_char] = "".join(alphabet_chars)

def get_error_status(selected_chars, cipher_table, curr_char, char_to_test):
    """Checks if at least one valid word can be found using the selected character.

    Args:
        selected_chars: the list of characters currently being deciphered

        cipher_table: the dictionary containing possible options for each letter

        curr_char: the specific cipher text character being tested

        char_to_test: the plaintext option for curr_char being tested

    Returns:
        True if the selected character resulted in no valid words.
    """
    complete_words = []
    for word in cipher_words:
        if (word[0] != '*' and curr_char in word and check_word_complete(word, selected_chars) and
            word not in complete_words):
            complete_words.append(word)

    complete_words.sort(key = len)
    for word in complete_words:
        valid = False
        permutation = {curr_char : char_to_test}

        # Gets unique letters in the word, with no repeats
        unique_letters = []
        for char in word:
            if char not in unique_letters:
                unique_letters.append(char)

        valid = valid or valid_permutation([word, unique_letters], 0, cipher_table,
                                           permutation, curr_char)
        if not valid:
            return True
    return False

def valid_permutation(word_data, index, cipher_table, permutation, char_to_skip):
    """Recursively checks every permutation for dictionary words

    Args:
        word_data: Index 0 is the word itself, index 1 is the unique letters found
        in that word.

        index: The index of the letter in word_data[1] being tested

        cipher_table: the dictionary containing possible options for each letter

        permutation: the current permutation of cipher to plaintext letters

        char_to_skip: the cipher text letter whose validity is being tested.
        This letter stays constant throughout the recursive loop.

    Returns:
        True if the current permutation resulted in a valid word
    """
    word = word_data[0]
    letters = word_data[1]
    if index >= len(letters):
        plain_word = ""
        for char in word:
            plain_word += permutation[char]
        return check_word_valid(plain_word)

    curr_char = letters[index]

    if curr_char == char_to_skip:
        if not char_unique(permutation[curr_char], curr_char, permutation):
            return False
        return valid_permutation(word_data, index + 1, cipher_table, permutation, char_to_skip)


    for char in cipher_table[curr_char]:
        if not char_unique(char, curr_char, permutation):
            continue
        permutation[curr_char] = char
        if valid_permutation(word_data, index + 1, cipher_table, permutation, char_to_skip):
            return True
        permutation[curr_char] = ""
    return False

def char_unique(char, curr_char, permutation):
    """Tests the uniqueness of char, as no two cipher text letters can
    have the same plaintext letter.

    Args:
        char: the plaintext char that must be unique in permutation

        curr_char: the cipher char being tested

        permutation: the current permutation of cipher to plaintext characters

    Returns:
        True if char cannot be found elsewhere in permutation
    """
    for key in permutation:
        if char in permutation[key] and key != curr_char:
            return False
    return True

def update_table(cipher_table):
    """Updates the table of possibilities once a letter is solved

    Args:
        cipher_table: the dictionary containing possible options for each letter
    """
    for key in cipher_table:
        if len(cipher_table[key]) == 1:
            if key in valid_chars:
                valid_chars.remove(key)
            for other_key in cipher_table:
                if key != other_key:
                    cipher_table[other_key] = cipher_table[other_key].replace(cipher_table[key], "")

def check_word_complete(word, selected_chars):
    """Checks if all letters in word have been selected

    Args:
        word: the word being tested

        selected_chars: the characters being tested

    Returns:
        True if every character in word can be found in selected_chars
    """
    for char in word:
        if char not in selected_chars:
            return False
    return True

def check_word_valid(word):
    """Searches the dictionary for word

    Args:
        word: the word being tested

    Returns:
        True if word can be found in the dictionary
    """
    print("Checking " + word + "...")
    if len(word) > 0 and word[0] == "*":
        return True
    if len(word) < SHORT_WORD_CUTOFF:
        return word in short_words
    return word in long_words

def get_plaintext(cipher_table):
    """Replaces the cipher text with its plaintext match.

    Args:
        cipher_table: The dictionary containing the cipher to plaintext translation.

    Returns:
        The newly deciphered plaintext.
    """
    to_return = ""
    for word in cipher_words:
        for letter in word.replace('*', ''):
            if cipher_table[letter] != "" and len(cipher_table[letter]) < 2:
                to_return += cipher_table[letter]
            else:
                to_return += "."
        to_return += " "
    return to_return

def print_ciphertext():
    """Prints the cipher text.
    """
    to_print = "Ciphertext:\t"
    for word in cipher_words:
        to_print += word + " "
    print (to_print)

def print_progress(cipher_table):
    """Helper method for readability to print the current result.

    Args:
        cipher_table: The dictionary containing the cipher to plaintext translation.
    """
    print()
    print(cipher_table)
    print()
    print("Plaintext:\t" + get_plaintext(cipher_table))
    print()
    print_ciphertext()
    print()
    print("Chars left: " + str(valid_chars))

if __name__ == "__main__":
    file_to_decrypt = sys.argv[1]
    print("Decrypting " + "\"" + file_to_decrypt + "\"")
    decrypt(file_to_decrypt)
