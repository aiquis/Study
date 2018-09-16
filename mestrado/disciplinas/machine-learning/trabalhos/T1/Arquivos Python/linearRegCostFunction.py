import numpy as np
from scipy.optimize import minimize


def linearRegCostFunction(theta, X, y, lamb):
    m = len(X)

    custo = ((1 / (2 * m)) * np.sum((X.dot(theta) - y) ** 2) +
             (lamb / (2 * m)) * np.sum(theta[1:]) ** 2)

    return custo


def linearRegGrad(theta, X, y, lamb):
    m = len(y)

    h = X.dot(theta)

    loss = h - y

    gradient = ((1 / m) * (X.T.dot(loss)) +
                (lamb / m) * theta[1:])

    return gradient


def trainLinearReg(theta, X, y, lamb):
    # initial_theta = np.zeros((X.shape[1],1))
    # initial_theta = np.array([[15], [15]])

    res = minimize(fun=linearRegCostFunction, x0=theta,
                   args=(X, y, lamb), method=None, jac=linearRegGrad,
                   options={'maxiter': 5000})

    return(res.x)
