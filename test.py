import numpy as np

a = np.array([0,1,2,3,4,5,6,7,8,9])
b = np.where(a>4,a,0)
print(b)