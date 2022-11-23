import numpy as np

from yachalk import chalk

def MatrixPowMatrix(m1, m2):
    try:
        result = []
        for v1, v2 in zip(m1, m2):
            result.append(v1**v2)
        return np.array(result)
    except:
        print(f"{chalk.red('Error')}")
        
x = np.array([1, 2, 3, 4, 5])       
y = np.array([1, 2, 3, 4, 5])    
test = MatrixPowMatrix(x, y)