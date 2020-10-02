# Jadon Schuler
# Generate prime numbers of a certain length using Miller-Rabin

import numpy as np
import secrets
import sys

output = "primes.txt"

def main():
    primes = []
    n_bits = 32

    for i in range(2):
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
            for j in range(128):
                if not millerrabin(n, d, r):
                    prime = False
                    break
            if prime:
                primes.append(n)

    string = ""
    for i in range(2):
        string += str(primes[i]) + "\t"
    string += "\n"
    for i in range(2):
        string += "{0:b}".format(primes[i]) + "\t"

    print("\n\n" + string)

    pq = primes[0] * primes[1]

    print("\np * q = " + str(pq))
    print("p * q = " + "{0:b}".format(pq))
    print(len("{0:b}".format(pq)))


def find_d_r(n: int):
    # Need to find d, r such that n - 1 = d * (2 ^ r)
    r = 0
    d = n - 1

    # Bitwise 'and' to test parity
    while d & 1 == 0:
        r += 1
        # Bitwise shift
        d = d >> 1

    return d, r

def millerrabin(n, d, r):
    a = 0
    while a < 2 or a == n - 1:
        a = secrets.randbelow(n)
    x = modular_exponentiation(a, d, n)
    print(str(a) + " ^ " + str(d) + "\t" + str(x))

    if x == 1 or x == n - 1:
        return True

    for i in range(1, r - 1):
        x = (x * x) % n
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def modular_exponentiation(base, power, modulus):
    result = 1
    while power > 0:
        if power & 1 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        power = power >> 1
    return result


if __name__ == "__main__":
    main()
