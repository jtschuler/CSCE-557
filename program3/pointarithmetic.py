# Jadon Schuler
# Copyright 2020

import sys
import ellipticpoints as ep

def main(a, b, prime):
    point_tuples = ep.find_points(a, b, prime)
    points = []
    for point in point_tuples:
        points.append(Point(point[0], point[1], 1, 'Affine'))
    max_order, max_point = find_max_order(points, a, b, prime)
    print('\nMax Order Point: ' + max_point.tuple_string() + '\tOrder: ' + str(max_order))

def find_max_order(points, a, b, prime):
    max = 0
    max_point = None

    for point in points:
        order = find_order(point, a, b, prime)
        if order > max:
            max = order
            max_point = point
    return max, max_point

def find_order(point, a, b, prime):
    print('\n\nSearching Point: ' + point.tuple_string())
    if point.z == 0:
        return 1

    p2 = double_point(point, a, b, prime)
    print(p2.to_string() + '\t' + p2.affine(31).to_string())
    # Starts at two since we've already done an addition
    count = 2
    while(p2.z != 0):
        count += 1
        p2 = add_points(p2, point, prime)
        print(p2.to_string() + '\t' + p2.affine(31).to_string())
    print('Order: ' + str(count))
    return count



def double_point(point, a, b, prime):
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
    """ point2 must have 1 as its Z coordinate!
    TODO
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


def modular_inverse(x, modulus):
    """REWORK W/ EXTENDED EUCLIDEAN ALGORITHM

    TODO

    """
    for i in range(1, modulus):
        y = (x * i) % modulus
        if y == 1:
            return i

    # i.e., not found
    return -1

class Point:
    def __init__(self, x, y, z, type='Jacobian'):
        self.x = x
        self.y = y
        self.z = z
        self.type = type
    def affine(self, prime):
        if self.z == 0:
            return self
        inv = modular_inverse(self.z, prime)
        x_a = (self.x * ep.modular_exponentiation(inv, 2, prime)) % prime
        y_a = (self.y * ep.modular_exponentiation(inv, 3, prime)) % prime
        return Point(x_a, y_a, 1, 'Affine')
    def to_string(self):
        return self.type + ': (' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'
    def tuple_string(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'


if __name__ == '__main__':
    print('\n\n')
    main(1, 3, 1000003)
