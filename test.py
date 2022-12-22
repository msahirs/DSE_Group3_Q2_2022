import numpy as np
from Wire_loading import split_eq_equation

a = np.array([[0,1,2,3,4],[5,6,7,8,9],[3,9,2,7,4]])
b = np.where(a>4,a,0)

K = np.array([[1,5,3,6],[9,3,7,1],[0,4,2,0],[5,3,9,8]])
P = np.ones(4)
R = np.zeros(4)
U = np.zeros(4)

split_vars = split_eq_equation(K, U, R, P)
print(split_vars['Kr'], split_vars['Pr'])
split_vars['Ur'] = np.linalg.inv(split_vars['Kr']).dot(split_vars['Pr'])
split_vars['Rs'] = split_vars['Ksr'].dot(split_vars['Ur']) - split_vars['Ps']

print("Try:", split_vars['Ur'], split_vars['Rs'])

# tup = split_eq_equation(K,U,R,P)
# print(K)
# print(tup)
