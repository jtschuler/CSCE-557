Jadon Schuler
CSCE 557
Copyright 2020

List of files:
2020program1.pdf
    The pdf containing the assignment details
allwords.txt
    A text file containing English dictionary words
automated_solver.py
    The automated decryption program
decrypted.txt
    The decrypted plaintext
fileio.py
    File input/output helper module
manual_solver.py
    The manual decryption program
README.txt
    This file
SubstitutionCipherProject.pdf
    Paper detailing my solution
zfileencryptzperm22.txt
    The original cipher text I was assigned
zfileencryptzperm22MODIFIED.txt
    The version of the cipher text I modified to work with the automated solver


These programs are meant to be used to solve simple substitution ciphers.
This project was built for Python 3.7.3
For more information, see SubstitutionCipherProject.pdf
See decrypted.txt for the decrypted version of zfileencryptzperm22.txt




To run the automated solver, run the following command in the command line:
python3 automated_solver.py zfileencryptzperm22MODIFIED.txt

NOTE: For the automated solver to work, all words MUST either be in the
dictionary or prepended with a star ('*'). This is why the modified text file
exists. I have gone through and manually added a star before every word not in
the dictionary.

After displaying letter frequency, the program allows for user-input cribbing,
at which point it loops over permutations until it finds the correct one. Once
readable plaintext is generated, the user is prompted to enter a file name in
which to print.

Because in a real world situation knowing that every word is in the dictionary,
or knowing which words to ignore would be inconvenient at best and impossible at
worst, I have provided a second program that requires user assistance to decrypt
the substitution cipher that can be run on the original cipher text (see below).




To run the manual solver, run the following command in the command line:
python3 manual_solver.py zfileencryptzperm22.txt

The program will repeatedly ask the user to make letter swaps until readable
plaintext is generated, at which point the user can end the loop. The user is
then prompted to enter a file name in which to print the generated plaintext.
