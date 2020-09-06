# Jadon Schuler
# CSCE 557
# Copyright 2020

"""This module focuses on cracking the substitution cipher.

This program is meant to be executed from the command line.
The second argument should be the filename to decrypt.
e.g. 'python solvecipher.py [the_file]'
"""

# Notes based on frequency and inspection
# q -> t
# m -> h
# x -> e

# s -> a
# i -> n
# w -> d

# a -> o
# u -> i


import sys
import fileio as fio

SHORT_WORD_CUTOFF = 5
ERROR_TOLERANCE = 5
valid_chars = []
unavailable_chars = []

plaintext_words = []
cipher_words = []
frequency = []

def decrypt(filename):
    # Reads and processes the cipher text
    cipher_text = fio.read_file_data(filename)
    words = cipher_text.split()
    for word in words:
        cipher_words.append(word)

    # Counts and displays letter frequency for cribbing
    count_letter_frequency(cipher_text)
    plaintext = decrypt_text()

    print("Decrypted text:")
    print(plaintext)
    filename = input("Enter the file you would like to write to: ")
    fio.write_to_file(filename, plaintext)

def count_letter_frequency(cipher_text):
    """Counts and returns the letter frequencies

    Args:
        cipher_text:
            The text whose letter frequency is to be counted

    Returns:
        letter_frequency:
            A dictionary with letters as keys and frequency as values
    """
    letter_frequency = {}
    for character in cipher_text:
        if character not in (' ', '\n'):
            if character not in letter_frequency:
                letter_frequency[character] = 1
            else:
                letter_frequency[character] += 1

    for character in letter_frequency:
        frequency.append([character, letter_frequency[character]])
        valid_chars.append(character)
    frequency.sort(reverse = True, key = lambda count: count[1])

def decrypt_text():
    # Initializes the decryption table
    cipher_table = {}
    for character in valid_chars:
        cipher_table[character] = "."

    print_progress(cipher_table)

    while True:
        next_char = input("Choose next char to replace or undo, or type print to print result to file: ")
        while next_char not in cipher_table and next_char != "print":
            next_char = input("Invalid, try again: ")

        if next_char == "print":
            break

        if cipher_table[next_char] == ".":
            print("Replacing " + next_char)
            valid_chars.remove(next_char)

            replacement = input("Choose char to replace with: ")
            while len(replacement) != 1 or replacement in unavailable_chars:
                replacement = input("Invalid or already selected, try again: ")
            cipher_table[next_char] = replacement
            unavailable_chars.append(replacement)
        else:
            print("Undoing " + next_char)
            valid_chars.append(next_char)
            unavailable_chars.remove(cipher_table[next_char])
            cipher_table[next_char] = "."

        print_progress(cipher_table)


    plaintext = get_plaintext(cipher_table)
    return plaintext


def replace_char(char_pair, cipher_table):
    cipher_table[char_pair[0]] = char_pair[1]

def get_plaintext(cipher_table):
    to_return = ""
    for word in cipher_words:
        for letter in word:
            if cipher_table[letter] != "" and len(cipher_table[letter]) < 2:
                to_return += cipher_table[letter]
            else:
                to_return += "."
        to_return += " "
    return to_return

def print_ciphertext():
    to_print = "Ciphertext:\t"
    for word in cipher_words:
        to_print += word + " "
    print (to_print)

def print_progress(cipher_table):
    print("\n\n\n\n\n\n\n\n\n\n")
    print_frequency()
    print()
    print("Plaintext:\t" + get_plaintext(cipher_table))
    print()
    print_ciphertext()
    print()
    print("Chars left: " + str(valid_chars))

def print_frequency():
    string = ""
    if len(frequency) > 0:
        string = frequency[0][0] + ": " + str(frequency[0][1])
    for i in range(1, len(frequency)):
        string += ", "
        string += frequency[i][0] + ": " + str(frequency[i][1])
    print(string)

if __name__ == "__main__":
    file_to_decrypt = sys.argv[1]
    print("Decrypting " + "\"" + file_to_decrypt + "\"")
    decrypt(file_to_decrypt)
