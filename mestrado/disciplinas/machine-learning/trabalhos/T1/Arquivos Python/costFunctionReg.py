import numpy as np
from sigmoide import sigmoide


def costFunctionReg(theta, X, y, alpha):

    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)

    grad0 = np.multiply(-y, np.log(sigmoide(X * theta.T)))
    grad1 = np.multiply((1 - y), np.log(1 - sigmoide(X * theta.T)))
    reg = (alpha / 2 * len(X)) * np.sum(np.asarray(
        theta[:, 1:theta.shape[1]]) ** 2)

    return np.sum(grad0 - grad1) / (len(X)) + reg
