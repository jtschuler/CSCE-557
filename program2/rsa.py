# Jadon Schuler
# Copyright 2020

"""This module implements RSA, given values for p, q, e, d, and the message to
encrypt, where p * q has at least 65 bits.

ASCII text is split into blocks of 8 characters. If this cannot be done evenly,
the message is padded with the null character ('\0'). Then, the program converts
each block into an integer. To encrypt, this integer is raised to the power e
modulo n. To decrypt, the integer is raised to the power d modulo n, then
converted back to ASCII.
"""


# Suppress variable name warning (my single-letter
# variables are meant to be that way)
# pylint: disable=C0103

import sys

# Imported for fast modular exponentiation implementation
import primegeneration as pg

def encrypt(p, q, e, d, text):
    """Main driver for implementing RSA

    Args:
        p: first prime
        q: second prime
        e: encryption exponent
        d: decryption exponent
    """
    n = p * q

    # Number of characters to pad with
    padding = 8 - (len(text) % 8)
    for i in range(padding):
        text += '\0'

    print("\n\nText to encrypt:\n" + text)

    print('\n\n\n......... Encryption .........')
    numblocks = int(len(text) / 8)
    e_message = []
    for i in range(numblocks):
        blocktext = text[i*8:(i + 1) * 8]
        print("\n\nBlock " + str(i) + ": " + blocktext)
        e_message.append(encrypt_block(blocktext, e, n))
        print("Encrypted ascii: " + integer_to_ascii(e_message[i]) + '\n')

    # Decryption
    print('\n\n\n......... Decryption .........')
    d_message = ''
    for i, block in enumerate(e_message):
        print("\n\nBlock " + str(i) + ": " + str(block))
        d_message += decrypt_block(block, d, n)

    print("\n\nDecrypted text:\n" + d_message + '\n')

def encrypt_block(blocktext, e, n):
    """Encrypts a block using RSA

    Args:
        blocktext: Block of 8 ASCII characters to encrypt
        e: encryption exponent
        n: modulus

    Returns:
        Encrypted block in integer representation
    """
    integer = ascii_to_integer(blocktext)
    encryption = pg.modular_exponentiation(integer, e, n)
    print("Encrypted integer:")
    print(str(integer) + " -> " + str(encryption))
    return encryption

def decrypt_block(encryption, d, n):
    """Decrypts a block using RSA

    Args:
        encryption: The encrypted integer representing a block of 8 ASCII chars
        d: decryption exponent
        n: modulus

    Retuns:
        The decrypted block in ASCII representation
    """
    decryption = pg.modular_exponentiation(encryption, d, n)
    print("Decrypted integer:")
    print(str(encryption) + " -> " + str(decryption))
    return integer_to_ascii(decryption)

def integer_to_ascii(integer):
    """Converts an integer into ASCII text

    Args:
        integer: integer representation of an 8 byte block of ASCII text

    Returns:
        The block of text represented by integer
    """
    string = ''
    print("\nTranslating letters...")
    for _ in range(8):
        letter = integer % 256
        integer = integer >> 8
        print("{0:08b}".format(letter) + " -> " + chr(letter))
        string = chr(letter) + string
    return string

def ascii_to_integer(text):
    """Converts a block of ASCII text into an integer

    Args:
        text: 8 character block of ASCII text

    Returns:
        Integer representation of the ASCII text
    """
    integer = 0
    for c in text:
        integer *= 256
        integer += ord(c)
    return integer

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please name an input file!")
        sys.exit()
    if len(sys.argv) > 2:
        print("Too many arguments specified!")
        sys.exit()
    input_file = open(sys.argv[1])
    args = input_file.readline().split()
    input_file.close()
    prime_one = int(args[0])
    prime_two = int(args[1])
    encryption_exp = int(args[2])
    decryption_exp = int(args[3])
    message = 'This is the message I would like to encrypt!'
    encrypt(prime_one, prime_two, encryption_exp, decryption_exp, message)
