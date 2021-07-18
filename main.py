# Steven Lam
# 2021
# %% Import modules
from shanks import SECP256K1, is_Prime, multiply_Points
from keygen import generate_256_hex

# %% Executing functions
# class SECP256k1 has two methods: find_Points() and show_Points()
pt = SECP256K1(87)
pt.find_Points()
pt.plot_Points()
# %%
pK = int(generate_256_hex(), 16)
multiply_Points()
# %%
# %%
