# Jadon Schuler
# Copyright 2020

# pylint: disable=C0103
# pylint: disable=R0912
# pylint: disable=R0914
# pylint: disable=R0915

"""This module runs the quadratic sieve to factor a large number
"""

import sys
import math

def factor(number, factor_base, sieve_length):
    """The main method of the program. Handles and stores all the data and calls
    other functions for calculations.

    Args:
        number: the number we want to factor
        factor_base: The factor base over which we will test for smoothness
        sieve_length: The value of k for our sieve which runs from [-k, k]
    """
    R = (int)(math.sqrt(number))
    print(R)

    logs = {}
    for prime in factor_base:
        logs[prime] = math.log(prime)

    print(factor_base)
    print(logs)

    offsets = {}
    for prime in factor_base:
        offsets[prime] = find_roots(prime, number, R)

    print(offsets)

    k = sieve_length

    sieve = [0] * (2 * k + 1)

    for prime in factor_base:
        for root in offsets[prime]:
            n = root - prime
            while n >= k * -1:
                sieve[n + k] += math.log(prime)
                n -= prime

            n = root
            while n <= k:
                sieve[n + k] += math.log(prime)
                n += prime

    val = math.log(number)/2 + math.log(k)
    sieve = [x - val for x in sieve]
    print(sieve)

    smooth_num_candidates = []
    tolerance = 10
    for i, value in enumerate(sieve):
        if abs(value) < tolerance:
            x = i - k
            q_x = (R + x)**2 - number
            smooth_num_candidates.append([q_x, x])

    print(smooth_num_candidates)

    smooth_nums = []

    for i, smooth in enumerate(smooth_num_candidates):
        factors = find_factors(smooth[0], factor_base)
        print((str)(smooth[0]) + ' ' + (str)(factors))
        if [0,0] not in factors:
            smooth_nums.append([smooth, factors])

    print('\n\n\nFinal Smooth Numbers:')
    for smooth in smooth_nums:
        print((str)(smooth[0][0]))

    ################ MATRIX FORMATION AND REDUCTION ###################

    size = len(factor_base) + 1

    if len(smooth_nums) < size:
        print('Not enough smooth numbers found!')
        sys.exit()

    matrix = [[0 for i in range(size)] for j in range(size)]
    companion = [[0 for i in range(size)] for j in range(size)]

    for i in range(size):
        companion[i][i] = 1
        for j in range(size):
            matrix[i][j] = smooth_nums[i][1][j][1] % 2

    print_matrix(matrix, companion, smooth_nums)

    matrix, companion = reduce_matrix(matrix, companion)

    print('\n\nFinal matrix:')
    print_matrix(matrix, companion, smooth_nums)

    zero_rows = find_zero_rows(matrix)
    print()
    print('Zero rows: ' + str(zero_rows))

    ######### BUILDING THE FACTORS ############
    for row in zero_rows:
        build_factors(row, companion, smooth_nums, number, factor_base)



def build_factors(row, companion, smooth_nums, number, factor_base):
    """This module builds factors from each zero row of the matrix.

    Args:
        row: Row number of zero row
        companion: the companion matrix
        smooth_nums: Our smooth numbers
        number: the number we are factoring
        factor_base: the factor base
    """
    print()
    print('Zero Row: ' + str(row))
    companion_row = companion[row]
    print(companion_row)

    product = 1
    a = 1
    R = (int)(math.sqrt(number))
    for i, value in enumerate(companion_row):
        if value == 1:
            product *= smooth_nums[i][0][0]
            a *= (smooth_nums[i][0][1] + R)

    print('Product: \t' + str(product))
    print('Congruence:\t' + str(a))

    b, factors = find_big_square_root(product, factor_base)
    print('Factors: ' + str(factors))
    print('a: ' + str(a) + '\tb: ' + str(b))

    plus = a % number + b % number
    minus = a % number - b % number

    print('Plus GCD:\t' + str(gcd(plus, number)))
    print('Minus GCD:\t' + str(gcd(minus, number)))
    print()

def gcd(a, b):
    """Simple GCD
    """
    if b == 0:
        return a
    return gcd(b, a % b)


def find_zero_rows(matrix):
    """Finds zero rows in a matrix

    Args:
        matrix: the matrix

    Returns:
        list of row numbers of zero rows
    """
    size = len(matrix)
    zero_rows = []

    for i in range(size):
        zero_row = True
        for j in range(size):
            if matrix[i][j] != 0:
                zero_row = False
                break
        if zero_row:
            zero_rows.append(i)
    return zero_rows


def reduce_matrix(matrix, companion):
    """Row reduction via Gaussian Elimination

    Args:
        matrix: the matrix
        companion: the companion matrix

    Returns:
        The matrix in reduced form and final companion matrix, both mod 2
    """
    # i is the pivot row
    size = len(matrix)
    rows = []

    for i in range(size):
        index = -1
        for j in range(i, size):
            if matrix[j][i] == 1 and (len(rows) == 0 or j not in rows):
                index = j
                rows.append(j)
                break
        if index == -1:
            print('No pivot found in column ' + str(i))
        else:   # i.e. pivot found
            print('Pivot on column ' + str(i) + ' row ' + str(index))
            for j in range(size):
                if j != index and matrix[j][i] == 1:
                    print('Adding row ' + str(index) + ' to row ' + str(j))
                    matrix = add_rows(matrix, index, j)
                    companion = add_rows(companion, index, j)
            matrix = mod_matrix(matrix)
    companion = mod_matrix(companion)
    return matrix, companion


def add_rows(matrix, row1, row2):
    """Helper method for Gaussian Elimination. Adds row 1 to row 2.
    """
    for i in range(len(matrix)):
        matrix[row2][i] += matrix[row1][i]
    return matrix


def mod_matrix(matrix):
    """Mods every value in matrix down by 2
    """
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            matrix[i][j] = matrix[i][j] % 2
    return matrix


def print_matrix(matrix, companion, smooth_nums):
    """Prints the matrix and companion matrix together
    """
    print()
    for i, row in enumerate(matrix):
        print((str)(smooth_nums[i][0][0]) + ':  \t' + (str)(row) + '\t' + str(companion[i]))


def find_factors(smooth_num, factor_base):
    """Finds factors of a smooth number candidate by way of trial division

    Args:
        smooth_num: The candidate for smoothness
        factor_base: The factor base

    Returns:
        the factors of smooth_num over the factor base, with a flag for true
        smoothness
    """
    number = smooth_num
    factors = []
    if number < 0:
        factors.append([-1,1])
        number *= -1
    else:
        factors.append([-1,0])

    for prime in factor_base:
        i = 1
        while number % prime**i == 0:
            i += 1
        i -= 1
        factors.append([prime, i])

    test = 1
    for prime_pair in factors:
        test *= prime_pair[0]**prime_pair[1]

    if test != smooth_num:
        factors.append([0,0])
    return factors

def find_big_square_root(square, factor_base):
    """Finds the square root of a smooth number

    Args:
        square: the square we want to find the root of
        factor_base: the factor base

    Returns:
        The square root and the factors of the square
    """
    root = 1
    factors = []
    for prime in factor_base:
        i = 1
        while square % prime**i == 0:
            i += 1
        i -= 1
        root *= prime**int(i/2)
        factors.append([prime, i])
    return root, factors



def find_roots(prime, number, R):
    """Finds the solutions to  (x + R)^2 - N congruent to 0 mod p

    Args:
        prime: The prime number
        number: The number we want to factor
        R: Integer square root (floor) of number

    Returns:
        the congruence solutions
    """
    roots = []
    for x in range(1, prime):
        q_x = (R + x)**2 - number
        if q_x % prime == 0:
            roots.append(x)
    return roots


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify an input file')
        sys.exit()
    if len(sys.argv) > 2:
        print('Too many arguments')
        sys.exit()

    primes_file = open('primes.txt')
    primes_list = list(map(int, primes_file.read().split()))
    primes_file.close()

    file = open(sys.argv[1])
    args = file.read().split()
    file.close()

    primes_list = primes_list[0:int(args[1])]

    factor(int(args[0]), primes_list, int(args[2]))
