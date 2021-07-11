# Steven Lam 
# 2021
# %%
import random
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import sys

# %%
def generate_256_hex():
    # generate random 256-bit hexadecimal number
    random_number = random.getrandbits(256) # generates random 256 bit number
    hex_number = hex(random_number) # returns number as hex string
    return hex_number[2:] # returns string after 0x

# check a point is on an elliptic curve
def on_curve(x, y):
    # secp256k1; y^2 = x^3 + 7
    if (x ** 3 + 7 - y ** 2)  == 0:
        return True
    else:
        return False

# %% 
def add_Points(p1, p2, p):
    """
    This is only for the elliptic curve y^2 = x^3 + 7
    """
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    if p1 != p2:
        s = ((y2 - y1) % p) * pow(((x2 - x1) % p), -1, p)
    else: # calculate tangent slope
        s = (3 * (x1 ** 2) % p) * pow((2 * y1) % p, -1, p)
        print(s)
    x3 = (s ** 2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return [x3, y3]

# TODO: Generator Point multiplication function
"""
args: G, k
where G = Generator point (constant) and k = int (private key)
Function will calculate P = k * G
"""

 # %%
def legendre_symbol(a, p):
    # euler criterion to compute legendre symbol 
    e = (p - 1) // 2
    if a % p == 0:
        return 0
    elif pow(a, e, p) == 1:
        return 1
    else:
        return -1

# %% Shanks Tonelli
def solve_QuadraticCongruence(a, p):
    # Step 1
    if p <= 2 or p % 2 == 0 :
        return 'None'
        # sys.exit('p must be a prime greater than 2. Exiting...')
    # Step 2
    ls = legendre_symbol(a, p)
    if ls != 1:
        return 'None'
        # sys.exit(f'{a} has no square root (mod {p}). Exiting...')
    # Step 3
    n = 1
    while ((p - 1) / (2 ** n)) % 2 == 0:
        n += 1
    k = ((p - 1) // (2 ** n))
    # Step 4
    q = 2
    while legendre_symbol(q, p) != -1:
        q += 1
    # Begin loop
    t = pow(a, (k + 1) // 2, p)
    r = pow(a, k, p)
    while True:
        i = 0
        while pow(r, pow(2, i), p) != 1:
            i += 1
        if i == 0:
            return [t, p - t]
        else:
            u = pow(q, k * pow(2, n - i - 1), p)
            t = (t * u) % p
            r = (r * u * u) % p

def is_Prime(p):
    for num in range(2,p):
        if p % num == 0:
            sys.exit("p is not a prime")

### Finding points on the secp256k1 curve
def find_Points(p):
    if p > 2 :
        is_Prime(p)
    else:
        sys.exit("p must be a prime and greater than 2")
    x_Points = []
    y_Points = []
    for x in range(p + 1):
        a =  x ** 3 + 7 # y2 = x3 + 7
        sol = solve_QuadraticCongruence(a, p) # output y for given x
        if sol == 'None':
            continue
        x_Points.append(x), y_Points.append(sol[0])
        x_Points.append(x), y_Points.append(sol[1])
    return x_Points, y_Points # Points in Galois Field

### Plot points on secp256k1 curve
def plot_Points(x_Points, y_Points):
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    plt.plot(x_Points, y_Points, 'o', color='black')
    plt.grid(which='both', axis='both')
    plt.xlim(0)
    plt.ylim(0)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    plt.show()

# %% Running functions
p = 17 # must be a prime number
x_Points, y_Points = find_Points(p)
plot_Points(x_Points, y_Points)
# %%
### Plotting elliptical curve over real numbers
y, x = np.ogrid[-6:6:50j, -6:6:50j]
a = 0
b = 7
p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - 1

plt.figure(figsize=(12,9))
plt.contour(x.ravel(), y.ravel(), pow(x, 3) + a*x + b - pow(y ,2), [0])
plt.grid()
plt.show()

# %% Multiply private key to generage public key
### Generate private key
priv_key = generate_256_hex()
print(priv_key)

# %%
## Resources
# https://en.bitcoin.it/wiki/Secp256k1
# https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc
# https://www.cs.purdue.edu/homes/ssw/cs655/ec.pdf
# https://asecuritysite.com/encryption/ecc_pointsv
# https://www.maa.org/sites/default/files/pdf/upload_library/22/Polya/07468342.di020786.02p0470a.pdf
