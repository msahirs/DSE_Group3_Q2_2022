import numpy as np
from Wire_loading import split_eq_equation

a = np.array([[0,1,2,3,4],[5,6,7,8,9],[3,9,2,7,4]])
b = np.where(a>4,a,0)

K = np.array([[1,5,3,6],[9,3,7,1],[0,4,2,0],[5,3,9,8]])
P = np.zeros(4)
R = np.zeros(4)
U = np.zeros(4)

tup = split_eq_equation(K,U,R,P)
print(K)
print(tup)
