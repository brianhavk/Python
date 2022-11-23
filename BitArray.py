import bitstring
import numpy as np

BitArray = bitstring.BitArray(float=1.0, length=32)
BitArrayBooleanList = list(BitArray)

BitArrayBinaryList = []
for item in BitArrayBooleanList:
    if(item==True):
        BitArrayBinaryList.append(1)
    if(item==False):
        BitArrayBinaryList.append(0)