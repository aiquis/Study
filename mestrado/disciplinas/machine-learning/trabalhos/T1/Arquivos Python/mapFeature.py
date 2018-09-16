import numpy as np


def mapFeature(x):

    registros = x.shape[0]

    for i in range(1, 6):
        for j in range(1, 6):
            new_features = np.multiply(x[:, 1] ** i, x[:, 2] ** j)
            new_features = np.reshape(new_features, (registros, 1))
            x = np.concatenate((x, new_features), axis=1)

    return x
