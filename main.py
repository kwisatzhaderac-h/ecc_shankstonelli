# %%
import random
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np

# %%
def generate_256_hex():
    # generate random 256-bit hexadecimal number
    random_number = random.getrandbits(256) # generates random 256 bit number
    hex_number = hex(random_number) # returns number as hex string
    return hex_number[2:] # returns string after 0x

# check a point is on an elliptic curve
def on_curve(x, y):
    # secp256k1; y^2 = x^3 + 7 , p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - 1 
    if (pow(x, 3) + 7 - pow(y ,2))  == 0:
        return True
    else:
        return False

def add_points(p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    if p1 != p2:
        s = (y2 - y1) / (x2 - x1)
    else: # calculate tangent slope
        s = (3*x1**2) / (2*y1)
    x3 = s**2 - x1 - x2
    y3 = s*(x1 - x3) - y1
    return [x3, y3]

# Finding all points on an elliptical curve
# mod function
# p must be an odd prime so check for prime
# x and y is in range 0 to p - 1, x, y = range(0, p)
# Naive approach
# Calculate all values of RHS for range x
# Calculate all values of LHS for range y
# Find where RHS % p == LHS % p 

# %%
generate_256_hex()

# %%
# Cryptography uses elliptic curves in a simplified form (Weierstrass form), which is defined as:
# y^2 = x^3 + ax + b
# Bitcoin uses the secp256k1 elliptic curve defined as:
# y2 = x3 + 7 , where a = 0 and b = 7

# The following plots the curve over real numbers

y, x = np.ogrid[-6:6:50j, -6:6:50j]
a = 0
b = 7
p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - 1

plt.figure(figsize=(12,9))
plt.contour(x.ravel(), y.ravel(), pow(x, 3) + a*x + b - pow(y ,2), [0])
plt.grid()
plt.show()

# pow(x, 3) + 7 - pow(y ,2)
# y = sqrt()

# %%
# Resources
# https://en.bitcoin.it/wiki/Secp256k1
# https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc
# https://www.cs.purdue.edu/homes/ssw/cs655/ec.pdf
# https://asecuritysite.com/encryption/ecc_pointsv
# Shanks - Tonelli Algorithm: https://www.maa.org/sites/default/files/pdf/upload_library/22/Polya/07468342.di020786.02p0470a.pdf