Jadon Schuler
October 21, 2020
CSCE 557: Introduction to Cryptography
Program 3: Elliptic Curve Arithmetic



List of files:
README.txt:     This file
input.txt:      Sample input for the program
findorders.py:  Finds points on an elliptic curve mod a prime, and calculates
                orders of each of the points on the elliptic curve



This program was made for Python 3.7



To use the program, run the following command:

python3 findorders.py input.txt

If running on something you expect to have a lot of output, my recommendation is
to redirect STOUT like so:

python3 findorders.py input.txt > output.txt

Any input file can be subbed in for 'input.txt,' however it must be formatted
such that arguments are on one line and space separated. The first argument must
be a, the second should be b, and the third should be the prime, where a and b
are the values that appear in the Weierstrauss equation for the elliptic curve.



Report:
In order to find points on the elliptic curve, my program iterates over x values
from 0 to one below the prime modulus (as the prime itself would be congruent to
zero). I then calculate the y^2 value using the Weierstrauss equation. In order
to efficiently check whether or not this value is a square modulo p, I first
find a primitive root. I then iterate through powers of this primitive root
until I get to the desired power. If the power is even, we know y^2 has 2
solutions mod p (unless y^2 = 0), which are the primitive root to half that
power and the modular 'negative' of that value. Of course, if the power is odd
then there is no point on the curve at that x value.

Once a point is found, we transform the point into the Jacobian coordinates to
make calculations a little simpler. We then use the equations from the book to
double the point, and then repeatedly add the new point to the initial point,
until we reach a new point with z = 0 (the point at infinity). The number of
point additions/doublings we performed is the order of that point, which we keep
track of and finally return.

To transform a Jacobian point back into Affine coordinates, we must utilize the
fact that a number times its modular inverse is 1, in order to avoid rational
numbers and division. To facilitate this, I included the extended Euclidean
algorithm from previous assignments to aid in finding modular inverses. Since
x' = x/z^2, we can multiply x' by the modular inverse of z twice to get back the
original x-value in Affine coordinates, and we follow a similar process for the
y value. The z value simply becomes 1.

I initially had my program find all points first, and THEN calculate the order
of each point, but it became clear very quickly on the prime 1000003 that this
wasn't feasible.

Instead, my program calculates the order of a point as it finds one so that one
doesn't have to wait an unreasonable amount of time just to START getting useful
results. That being said, running on a large prime like 1000003 will still take
a lot of time since the arithmetic is costly. However, I am fairly certain it is
correct, since the powered up points still appear to be solutions on the curve.
