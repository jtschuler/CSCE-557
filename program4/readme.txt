Jadon Schuler
November 17, 2020
CSCE 557: Introduction to Cryptography
Program 4: Quadratic Sieve




List of files:
readme.txt:         This file
input.txt:          Sample input for the program
primes.txt:         A list of prime numbers
quadraticsieve.py:  Runs the quadratic sieve to factor a large number



This program was made for Python 3.7



To use the program, run the following command:

python3 quadraticsieve.py input.txt



Any input file can be used in place of 'input.txt,' however it must be formatted
such that arguments are on one line and space separated. The first argument must
be the number you want to factor, the second should be the number of small
primes in the factor base, and the third should be the length of the sieve
array.



Report:
Since I didn't want to have to deal with larger powers of primes, I used the
method outlined in Silverman's paper in order to find my smooth numbers. To find
the smooth numbers, I first generated a list of possible candidates using that
method with a rather wide tolerance, and then factored each candidate via a
variant of trial division (to work with large numbers) to see whether or not the
number was truly smooth.

Once I determined the smooth numbers, I set up the matrix and companion identity
matrix, then performed a simple algorithm for Gaussian elimination. Then I
iterated over any zero rows to build products from them using the corresponding
companion row and the offsets (R + n). I then took the square root of the
product to get my first square root, and the product of the offsets was the
second square root. I then performed the GCD on both of these numbers with the
number we wanted to factor to get the final factors.
