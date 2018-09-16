import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from custo_reg_lin_uni import custo_regressao_linear

# Valores de theta0 e theta1 informados no enunciado do trabalho
theta0 = np.arange(-10, 10, 0.01)
theta1 = np.arange(-1, 4, 0.01)

# Inicia os valores de J com zeros
J = np.zeros((len(theta0), len(theta1)))

# Preenche os valores sucessivos de J
for i in range(len(theta0)):
    for j in range(len(theta1)):
        t = [[theta0[i]], [theta1[j]]]
        J[i,j] = custo_regressao_linear(x, y, t)

# Transpõe J devido as funções contour/meshgrid
J = np.transpose(J)

# Plota a função de custo utilizando levels como logspace. Range -1 ~ 4 devido ao
# range de theta1 e 20 pois o theta0 tem 20 valores (-10 até 10)
fig = plt.figure()
fig, ax = plt.subplots()
ax.contour(theta0, theta1, J, levels=np.logspace(-1, 4, 20), color='blue')
ax.plot(theta[0,0], theta[1,0], 'rx')
plt.xlabel('theta0')
plt.ylabel('theta1')
plt.show()