# Jadon Schuler
# Copyright 2020

# pylint: disable=C0103
# pylint: disable=W1114

"""This module finds the orders of points on an elliptic curve mod a prime p
"""

import sys
import findpoints as fp

def main(a, b, prime):
    """Main function

    Args:
        a: the elliptic curves' a value
        b: the elliptic curve's b value
        prime: the modulus
    """
    point_tuples = fp.find_points(a, b, prime)
    points = []
    for point in point_tuples:
        points.append(Point(point[0], point[1], 1, 'Affine'))
    max_order, max_point = find_max_order(points, a, prime)
    print('\nMax Order Point: ' + max_point.tuple_string() + '\tOrder: ' + str(max_order))

def find_max_order(points, a, prime):
    """Finds the max order and associated point in points

    Args:
        points: List of points on the elliptic curve
        a: the elliptic curve's a value
        prime: the modulus

    Returns:
        The max order and the point it was found at
    """
    max_order = 0
    max_point = None

    for point in points:
        order = find_order(point, a, prime)
        if order > max_order:
            max_order = order
            max_point = point
    return max_order, max_point

def find_order(point, a, prime):
    """Finds the order of a point on an elliptic curve

    Args:
        point: the point
        a: the elliptic curve's a value
        prime: the modulus

    Returns:
        the order of the point
    """
    print('\n\nSearching Point: ' + point.tuple_string())
    if point.z == 0:
        return 1

    p2 = double_point(point, a, prime)
    print(p2.to_string() + '\t' + p2.affine(31).to_string())
    # Starts at two since we've already done an addition
    count = 2
    while p2.z != 0:
        count += 1
        p2 = add_points(p2, point, prime)
        print(p2.to_string() + '\t' + p2.affine(31).to_string())
    print('Order: ' + str(count))
    return count



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
        x_a = (self.x * fp.modular_exponentiation(inv, 2, prime)) % prime
        y_a = (self.y * fp.modular_exponentiation(inv, 3, prime)) % prime
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
