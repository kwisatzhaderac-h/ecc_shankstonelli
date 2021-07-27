# Steven Lam
# 2021
# %% Import modules
from shanks import SECP256K1, is_Prime, multiply_Points
from keygen import generate_256_hex

if __name__ == "__main__":
    # class SECP256k1 has two methods: find_Points() and show_Points()
    p = int(input("Please enter a prime number greater than 2: "))
    pt = SECP256K1(p)
    pt.plot_Points()
else:
    # Executing functions
    # TODO: show random hex key and multiply it with curve
    pK = int(generate_256_hex(), 16)
    multiply_Points()
# %%
