CSCE 557 Programming Assignment 2
Jadon T Schuler
Due Oct 6, 2020

List of Files:
primegeneration.py: 	Python script for generating primes and encryption/decryption exponents
rsa.py:			Python script for encrypting and decrypting text using RSA
input.txt:		Sample output of primegeneration.py and sample input for rsa.py
text.txt:		Sample input ASCII text for rsa.py
README.txt:		This file

This project was built for Python3
Dependencies: secrets

Instructions:
To generate prime numbers, as well as the decryption/encryption exxponents, please run the following command:
python3 primegeneration.py

The program will search for 2 prime numbers (p and q) of size n_bits, then prompt the user for an encryption
exponent coprime to (p - 1)(q - 1). If a valid exponent is input, the program will calculate the decryption
exxponent. Lastly, the program will prompt the user for a filename to print into, and print all four items
on a single line. For example output, see 'input.txt'


To run RSA encryption/decryption, run the following command:
python3 rsa.py [file1] [file2]

Where [file1] is the filename containing the primes, encryption, and decryption exponents space-separated on
a single line, and [file2] is an ASCII text file whose content is to be encrypted. I have included a few
error checks to ensure the input is formatted correctly.

The program will not print to a file, but will instead print the results to the console.



Description:
To generate prime numbers, I used the Miller-Rabin method, which is based on an extension of Fermat's Little
Theorem. Namely, if a prime number forms a multiplicative group, that group must not have any non-trivial
square roots of unity. For an odd candidate, the program runs Miller-Rabin many times as it is a probabilistic
algorithm. Although not quite ensured, we can be reasonably certain that any numbers found are prime. Just to
be safe, I checked the numbers I found for 'input.txt' against a list of prime numbers up to 1000 billion to
ensure they were actually prime. Next, we select our encryption and decryption exponents. Once we have chosen
an e that is coprime (p - 1)(q - 1) = phi_n, we run the extended Euclidean algorithm to determine the x and y
such that ax + by = GCD, in our case ax + by = 1. If we replace a with e and b with phi_n, the x we get should
be d. Once we have these four numbers, we're ready to run RSA.

First, we block the text into blocks of 8 characters of ASCII text. If there are too few characters, we pad with
the null character, '\0' until the number of characters is divisible by 8. Then, for each block, we encode from
left to right by building up an integer representation for the block. If we start with m = 0, we add the ASCII
value of the left character to m, then multiply m by 256. We then repeat the process for each character in the
block. In this way, we build up a 64 bit integer. Since our modulus is at least 65 bits, we know that each 64
bit integer will have a unique value once we exponentiate it to the power e mod n.

To decrypt, we reverse the process. We have chosen e * d = 1 mod phi_n, so we know that any number raised to the
power (e * d) mod n is itself. For each blocked integer, we exponentiate to the power d mod n to get back the
original integer. Then, we decode from right to left. We take the rightmost 8 bits, decode the ASCII character,
and add that character to the beginning of the string we are building up. Then, we bitshift the integer right 8
bits. We repeat the process seven more times to get all 8 characters, then return the string, which is appended
to the running message. Once this has been done for every block, the original message is decoded.
