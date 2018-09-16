import pandas as pd
import numpy as np
from mapFeature import mapFeature
from costFunctionReg import costFunctionReg
from gradRegLog import gradRegLog
import scipy.optimize as opt
import matplotlib.pyplot as plt


dataset = pd.read_csv("ex2data2.txt", header=None,
                      names=['teste1', 'teste2', 'resultado'])
dataset.insert(0, 'Ones', 1)
dataset = np.array(dataset)
cols = dataset.shape[1]
X = dataset[:, 0:cols - 1]
y = dataset[:, cols - 1:]


new_x = mapFeature(X)
# print(new_x)

theta = np.zeros(len(new_x.T))
print(theta)

custo = costFunctionReg(theta, new_x, y, 1)
print(custo)

# opt_theta = opt.fmin_tnc(func=costFunctionReg, x0=theta,
#                         fprime=gradRegLog, args=(new_x, y, 1))
opt_theta = gradRegLog(theta, new_x, y, 1)
print(np.array(opt_theta))
