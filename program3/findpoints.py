# Jadon Schuler
# Copyright 2020

# pylint: disable=C0103

"""This module finds points on an elliptic curve modulo a prime number.
"""

import sys

def find_points(a, b, prime):
    """Finds points on the elliptic curve mod prime

    Args:
        a: The a value of the elliptic curve
        b: The b value of the elliptic curve
        prime: the prime modulus

    Returns:
        the list of points on the curve
    """
    proot = find_root(prime)
    if proot == -1:
        print('No primitive root found!')
        sys.exit()

    print('Points on the curve\t' + 'a: ' + str(a) + '\tb: ' +
            str(b) + '\tprime: ' + str(prime))
    print('Primitive root: ' + str(proot))

    points = []
    for x in range(prime):
        ysquare = (x**3 + a * x + b) % prime
        y = check_square(ysquare, prime, proot)
        if y != -1:
            y_neg = prime - y

            point1 = (x, y)
            point2 = (x, y_neg)

            if y_neg < y:
                point1 = (x, y_neg)
                point2 = (x, y)

            if point1 not in points:
                points.append(point1)
                print('Point:\t(' + str(point1[0]) +
                    ', ' + str(point1[1]) + ')')
            if point2 not in points:
                points.append(point2)
                print('Point:\t(' + str(point2[0]) +
                    ', ' + str(point2[1]) + ')')

    return points


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

def check_square(x, prime, proot):
    """Checks if x is a square modulo prime

    Args:
        x: the number to be checked
        prime: the prime
        proot: the primitive root of prime

    Returns:
        The root if it exists, else -1
    """
    result = proot
    exp = 1
    while result != x:
        result = (result * proot) % prime
        exp += 1
    if (exp & 1) == 0:
        exp = exp >> 1
        return modular_exponentiation(proot, exp, prime)
    return -1

def find_root(prime):
    """Finds a primitive root of prime

    Args:
        prime: the prime

    Returns:
        the lowest primitive root of prime
    """
    for i in range(1, prime):
        exp = 1
        for _ in range(prime - 2):
            exp = (exp * i) % prime
            if exp == 1:
                break
        if exp != 1:
            return i
    return -1
