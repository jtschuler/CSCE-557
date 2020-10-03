

import primegeneration as pg
import secrets
import sys

def main(p, q, d, e):
    n = p * q
    y = pg.modular_exponentiation(3, e, n)
    z = pg.modular_exponentiation(y, d, n)
    print(z)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please name an input file!")
        exit()
    if len(sys.argv) > 2:
        print("Too many arguments specified!")
        exit()
    input = open(sys.argv[1])
    args = input.readline().split()
    input.close()
    p = int(args[0])
    q = int(args[1])
    e = int(args[2])
    d = int(args[3])
    main(p, q, d, e)
