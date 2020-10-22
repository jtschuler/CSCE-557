# Jadon Schuler
# Copyright 2020

# pylint: disable=C0103
# pylint: disable=W1114
# pylint: disable=R0914

"""This module finds the orders of points on an elliptic curve mod a prime p
"""

import sys

def main(a, b, prime):
    """Finds points and calculates each point's order

    Args:
        a: the elliptic curves' a value
        b: the elliptic curve's b value
        prime: the modulus
    """

    proot = find_root(prime)
    if proot == -1:
        print('No primitive root found!')
        sys.exit()

    print('Points on the curve\t' + 'a: ' + str(a) + '\tb: ' +
            str(b) + '\tprime: ' + str(prime))
    print('Primitive root: ' + str(proot))

    max_order = 0
    max_point = None
    for x in range(prime):
        ysquare = (x**3 + a * x + b) % prime
        y = check_square(ysquare, prime, proot)
        if y != -1:
            y_neg = prime - y

            point1 = Point(x, y, 1, 'Affine')
            point2 = Point(x, y_neg, 1, 'Affine')

            if y_neg < y:
                point1 = Point(x, y_neg, 1, 'Affine')
                point2 = Point(x, y, 1, 'Affine')

            order1, points1 = find_order(point1, a, prime)

            print('\n\nSearching Point: ' + point1.tuple_string() + '\tOrder: ' + str(order1))
            for i, p in enumerate(points1):
                print('M: ' + str(i+2) + '\t' + p.to_string() + '\t' + p.affine(prime).to_string())


            order2, points2 = find_order(point2, a, prime)

            print('\n\nSearching Point: ' + point2.tuple_string() + '\tOrder: ' + str(order2))
            for i, p in enumerate(points2):
                print('M: ' + str(i+2) + '\t' + p.to_string() + '\t' + p.affine(prime).to_string())

            if order1 > max_order:
                max_order = order1
                max_point = point1

            if order2 > max_order:
                max_order = order2
                max_point = point2

    # Max order point of ALL the points
    print('\nMax Order Point: ' + max_point.tuple_string() + '\tOrder: ' + str(max_order))



def find_order(point, a, prime):
    """Finds the order of a point on an elliptic curve

    Args:
        point: the point
        a: the elliptic curve's a value
        prime: the modulus

    Returns:
        the order of the point
    """

    if point.z == 0:
        return 1

    points = []

    p2 = double_point(point, a, prime)
    points.append(p2)
    # Starts at two since we've already done an addition
    count = 2
    while p2.z != 0:
        count += 1
        p2 = add_points(p2, point, prime)
        points.append(p2)
    return count, points



def double_point(point, a, prime):
    """Function to double a point on an elliptic curve

    Args:
        point: the point
        a: the elliptic curve's a value
        prime: the modulus

    Returns:
        the new point
    """
    A = point.y**2

    B = point.x * A
    B = B << 2

    C = A**2
    C = C << 3

    D = 3 * point.x**2 + a * point.z**4

    x3 = B << 1
    x3 = D**2 - x3

    y3 = D * (B - x3) - C

    z3 = point.y * point.z
    z3 = z3 << 1

    return Point(x3 % prime, y3 % prime, z3 % prime)



def add_points(point1, point2, prime):
    """Function to add two points on an elliptic curve

    NOTE: point2's z-value MUST be 1

    Args:
        point1: the first point
        point2: the second point
        prime: the modulus

    Returns:
        the order of the point
    """

    A = point1.z**2
    B = point1.z * A
    C = point2.x * A
    D = point2.y * B
    E = C - point1.x
    F = D - point1.y
    G = E**2
    H = G * E
    I = point1.x * G

    x3 = I << 1
    x3 = F**2 - H - x3

    y3 = F * (I - x3) - point1.y * H

    z3 = point1.z * E

    return Point(x3 % prime, y3 % prime, z3 % prime)



def modular_inverse(num, prime):
    """Finds modular inverse of x mod prime

    Args:
        num: the number we want to invert
        prime: the modulus

    Returns:
        x % n: the decryption exponent associated with e
    """
    _, x, _ = extended_euclidean(num, prime)
    return x % prime



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
    if b == 0:
        return a, 1, 0
    # a - bq = r
    q = a // b
    gcd, x, y = extended_euclidean(b, a % b)
    return gcd, y, x - q * y



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
    if x == 1:
        return 1
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



class Point:
    """Class for holding a point's data
    """
    def __init__(self, x, y, z, kind='Jacobian'):
        """Instantiates a point
        """
        self.x = x
        self.y = y
        self.z = z
        self.kind = kind
    def affine(self, prime):
        """Returns the affine representation mod prime
        """
        if self.z == 0:
            return self
        inv = modular_inverse(self.z, prime)
        x_a = (self.x * modular_exponentiation(inv, 2, prime)) % prime
        y_a = (self.y * modular_exponentiation(inv, 3, prime)) % prime
        return Point(x_a, y_a, 1, 'Affine')
    def to_string(self):
        """Create string
        """
        return self.kind + ': (' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'
    def tuple_string(self):
        """Create string
        """
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify an input file')
        sys.exit()
    if len(sys.argv) > 2:
        print('Too many arguments')
        sys.exit()

    file = open(sys.argv[1])
    args = file.read().split()
    file.close()

    # Argument 1 is a, 2 is b, and 3 is the prime number
    main(int(args[0]), int(args[1]), int(args[2]))
