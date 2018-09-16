import numpy as np


def normalizar_caracteristicas(X, y):
    mean_X = np.mean(X, axis=0)
    std_X = np.std(X, axis=0)
    X_norm = (X - mean_X) / std_X

    mean_y = np.mean(y, axis=0)
    std_y = np.std(y, axis=0)
    y_norm = (y - mean_y) / std_y

    # Armazenando os valores utilizados para a normalização para
    # referência futura
    norm_values = {"mean_X": mean_X,
                   "std_X": std_X,
                   "mean_y": mean_y,
                   "std_y": std_y}

    return X_norm, y_norm, mean_X, std_X, mean_y, std_y, norm_values
