import scipy.io as spio
import matplotlib.pyplot as plt
from linearRegCostFunction import (linearRegCostFunction, linearRegGrad,
                                   trainLinearReg)
import numpy as np


# 5.1 - Visualizacao dos dados
mat = spio.loadmat('ex5data1.mat', squeeze_me=True)

X = mat['X']
y = mat['y']

Xtest = mat['Xtest']
ytest = mat['ytest']

Xval = mat['Xval']
yval = mat['yval']

plt.scatter(X, y, color='red', marker='x')
plt.xlabel('Change in water level (x)')
plt.ylabel('Water flowing out of the dam (y)')
plt.show()

# 5.2 - Funcao de custo da regressao linear regularizada

X_ones = np.c_[np.ones(X.shape[0]), X]

theta = np.ones(2)
custo = linearRegCostFunction(theta, X_ones, y, 0)
print(custo)

# 5.3 - Gradiente na regressao linear regularizada

grad = linearRegGrad(theta, X_ones, y, 0)
print(grad)

opt_theta = trainLinearReg(theta, X_ones, y, 0)
print(opt_theta)

grad = grad.T
t = np.linspace(X.min(), X.max())
h = np.c_[np.ones(t.shape[0]), t].dot(grad)

plt.scatter(X, y, marker='x', color='red')
# Corrigir para receber os parâmetros de theta otimizados
plt.plot(t, opt_theta[0] + (opt_theta[1] * t), color='blue',
         label='Linear Regression')
plt.axis([-50, 40, -5, 40])
plt.xlabel('Change in water level (x)')
plt.ylabel('Water flowing out of the dam (y)')
plt.show()
