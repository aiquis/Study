import numpy as np
from linearRegCostFunction import trainLinearReg, linearRegCostFunction


def learningCurve(X, y, Xval, yval, lamb):
    m = len(y)

    erro_train = np.zeros((m, 1))
    erro_val = np.zeros((m, 1))

    theta = np.zeros(2)

    for i in range(m):
        res = trainLinearReg(theta, X[:i + 1], y[:i + 1], lamb)
        erro_train[i] = linearRegCostFunction(res, X[:i + 1],
                                              y[:i + 1], lamb)
        erro_val[i] = linearRegCostFunction(res, Xval, yval, lamb)

    return(erro_train, erro_val)
