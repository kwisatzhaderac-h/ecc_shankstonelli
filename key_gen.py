# Steven Lam 
# 2021
# %%
import random

def generate_256_hex():
    # generate random 256-bit hexadecimal number
    random_number = random.getrandbits(256) # generates random 256 bit number
    hex_number = hex(random_number) # returns number as hex string
    return hex_number[2:] # returns string after 0x

# %%