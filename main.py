# Steven Lam 
# 2021
# %%
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import sys

# check a point is on an elliptic curve
def on_Curve(pt, p):
    """
    Checks if x,y lies on the curve secp256k1; y^2 = x^3 + 7 (mod p)
    """
    x, y = pt
    if (x ** 3 + 7 - y ** 2) % p == 0:
        return True
    else:
        return False

def is_Prime(p):
    for num in range(2,p):
        if p % num == 0:
            sys.exit("p is not a prime")


def add_Points(p1, p2, p):
    """
    Point addition for curve secp256k1 y^2 = x^3 + 7 (mod p)
    """
    x1, y1 = p1
    x2, y2 = p2
    if p1 == [0, 0]:
        return p2
    elif p2 == [0, 0]:
        return p1 
    elif p1 != p2:
        num = (y2 - y1) % p
        den = (x2 - x1) % p
    else: # calculate tangent slope
        num = 3 * (x1 ** 2) % p
        den = (2 * y1) % p
    # check for point at infinity
    if den == 0:
        return [0, 0]
    s = num * pow(den, -1, p)
    x3 = (s ** 2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return [x3, y3]

def multiply_Points(G, k, p):
    """
    args: G, k
    where G = Generator point (constant) and k = int (private key)
    Function will calculate P = G * k
    for curve sep256k1 (mod p)
    """
    assert on_Curve(G[0], G[1], p) == True, "Point G does not lie on the curve."
    if k == 1:
        return G
    if k == 0:
        return 0
    p1 = G
    for i in range(2, k + 1):
        p1 = add_Points(p1, G, p)
    return p1

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

## Resources
# https://en.bitcoin.it/wiki/Secp256k1
# https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc
# https://www.cs.purdue.edu/homes/ssw/cs655/ec.pdf
# https://asecuritysite.com/encryption/ecc_pointsv
# https://www.maa.org/sites/default/files/pdf/upload_library/22/Polya/07468342.di020786.02p0470a.pdf
