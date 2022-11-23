import math
import numpy as np

A = 5
B = 0

EA = 14.300
EB = 14.900

ΔBA = abs(B-A)
ΔE = abs(EB - EA)

Distance = math.sqrt(ΔBA**2 + ΔE**2) 
Surface_Position = Distance/2
