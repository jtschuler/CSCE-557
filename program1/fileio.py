# Jadon Schuler
# CSCE 557
# Copyright 2020

"""This module is used for file input and output.

The first function is used for getting the cipher-
text from the desired file, and the second method
is used for writing the deciphered text to a new file

Usage:
    some_string = read_file_data(some_file)
    write_to_file(some_file, some_text)
"""

def read_file_data(filename):
    """Gets the cipher text from a file"""
    cipher_file = open(filename, "r")
    cipher_text = cipher_file.read()
    cipher_file.close()
    return cipher_text

def get_dictionary_words():
    """Gets the words from the dictionary file"""
    dictionary = open(r"allwords.txt", "r")
    dictionary_text = dictionary.read()
    words = dictionary_text.split()
    dictionary.close()
    return words

def write_to_file(filename, plaintext):
    """Writes the deciphered plaintext to a new file"""
    plain_file = open(filename, "w")
    plain_file.write(plaintext)
    plain_file.close()
