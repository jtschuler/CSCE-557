# Jadon Schuler
# Copyright 2020

"""This module finds primes, and encryption and decryption exponents for RSA

This module uses the Miller-Rabin method to generate two prime numbers of size
n_bits bits, which by default is 32. Then, after calculating n = p * q, the
program prompts the user for a value of e, which must be coprime to phi_n, then
solves the extended euclidean algorithm to find d. The program then prompts the
user for the name of a text file, and prints to that text file.
"""

# Suppress variable name warning (my single-letter
# variables are meant to be that way)
# pylint: disable=C0103

# Suppress argument out of order warning (incorrect warning in GCD function)
# pylint: disable=W1114

# Used for random number generation
import secrets

def main():
    """Main function for running Miller-Rabin and exponent finding.
    """
    primes = []
    n_bits = 32

    for _ in range(2):
        prime = False
        while not prime:
            # Generate a random int of length n_bits bits
            n = secrets.randbits(n_bits)
            n = n | 2**n_bits

            # Ensure n odd
            if n & 1 == 0:
                n += 1

            # Find d, r for which n - 1 = d * (2 ^ r)
            d, r = find_d_r(n)

            print("N\t" + str(n))
            print("N_2\t" + "{0:b}".format(n))
            print("d\t" + str(d))
            print("r\t" + str(r))
            print("N = " + str(d) + " * (2 ^ " + str(r) + ")")

            prime = True
            for _ in range(128):
                if not millerrabin(n, d, r):
                    prime = False
                    break
            if prime:
                primes.append(n)

    print("\n\np: " + str(primes[0]) + "\tq: " + str(primes[1]))

    p = primes[0]
    q = primes[1]

    n = p * q
    phi_n = (p - 1) * (q - 1)

    print("\nn = " + str(n))
    print("phi_n = " + str(phi_n))
    print(str(len("{0:b}".format(n))) + " bits in length\n\n")


    print("Encryption and Decryption Exponentiation:")
    e, d = find_decryption(phi_n)
    print("Decryption exponent found!")
    print("e: " + str(e) + "\td: " + str(d))

    print("Printing to file...")
    filename = input("Enter desired filename: ")
    file = open(filename, "w")
    file.write(str(p) + ' ' + str(q) + ' ' + str(e) + ' ' + str(d) + '\n')
    file.close()

def find_d_r(n: int):
    """Finds d and r such that n - 1 = d * (2 ^ r)

    Args:
        n: the number for which to solve the equation

    Returns:
        d: d in the above equation
        r: r in the above equation
    """
    r = 0
    d = n - 1

    # Bitwise 'and' to test parity
    while d & 1 == 0:
        r += 1
        # Bitwise shift
        d = d >> 1

    return d, r

def millerrabin(n, d, r):
    """Tests n given d and r for primality

    Miller-Rabin takes advantage of the fact that there are no trivial roots of
    unity mod n when n is prime.

    Args:
        n: The prime number candidate
        d: d such that n - 1 = d * (2 ^ r)
        r: r such that n - 1 = d * (2 ^ r)

    Returns:
        False if n is definitely composite, true otherwise
    """
    a = 0
    while a < 2 or a == n - 1:
        a = secrets.randbelow(n)
    x = modular_exponentiation(a, d, n)
    print(str(a) + " ^ " + str(d) + "\t" + str(x))

    if x in (1, n - 1):
        return True

    for _ in range(1, r - 1):
        x = (x * x) % n
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False

# From here on related to finding d from e
def find_decryption(n):
    """Finds decryption exponent given n and user-input e

    Choice of e must be coprime to n! Continues to prompt until this is true.

    Args:
        n: the order of the group formed by p * q, or phi_n

    Returns:
        e: the valid encryption exponent
        x % n: the decryption exponent associated with e
    """
    # ex - ny = 1
    e = int(input("Enter choice for e: "))
    gcd, x, _ = extended_euclidean(e, n)
    while gcd != 1:
        print("Choice of e is not coprime to phi_n!\nGCD: " + str(gcd))
        e = int(input("\nPlease enter a different choice for e: "))
        gcd, x, _ = extended_euclidean(e, n)
    return e, x % n

def extended_euclidean(a, b):
    """The extended euclidean algorithm

    Recursively determines the GCD, as well as the x and y that satisfy
    ax + by = GCD

    Args:
        a: the first number
        b: the second number

    Returns:
        gcd: the GCD
        x, y: the x and y that satisfy the extended linear combination
    """
    if b > a:
        return extended_euclidean(b, a)
    if b == 0:
        return a, 0, 1
    # a - bq = r
    q = a // b
    gcd, x, y = extended_euclidean(b, a % b)
    return gcd, y - q * x, x


def modular_exponentiation(base, power, modulus):
    """Efficient modular exponentiation

    Args:
        base: the base
        power: the power
        modulus: the modulus

    Returns:
        The result of base ^ power (mod modulus)
    """
    result = 1
    while power > 0:
        if power & 1 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        power = power >> 1
    return result


if __name__ == "__main__":
    main()
