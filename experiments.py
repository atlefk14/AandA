stringen = b'\x00\x00\x01\x00'
stringen = b'\x00\x00\xff\xff'

print(int.from_bytes(stringen, signed=True, byteorder='little'))

from bitstring import BitArray
import numpy as np
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val
bits = str(BitArray(bytes=stringen).bin)
x = list(bits)
x = np.array(x, dtype=int)

bits = ""
for i in x:
    bits +=str(i)


bytes = BitArray(bin=bits).bytes
print(bytes)

print(twos_comp(int(bits, 2), len(bits)))

