import numpy as np
import matplotlib.pyplot as plt
import scipy.io


def normalize_features(X):
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)
    normalized_X = np.divide(X - mu, sigma)

    return (normalized_X, mu, sigma)


def pca(X):
    # Transforma X numa matriz pra permitir calculo do produto
    # com seu transposto
    X = np.matrix(X)
    m = X.shape[0]
    # Calculando a matriz de covariancia dos dados
    sigma = np.dot(X.T, X) / m
    # Aplicando a decomposição de valores singulares para
    # computar os componentes principais
    U, S, V = np.linalg.svd(sigma)
    return (U, S)


def project_data(X, U, K):
    U_reduce = U[:, 0:K]
    Z = np.zeros((len(X), K))
    for i in range(len(X)):
        x = X[i, :]
        projection_k = np.dot(x, U_reduce)
        Z[i] = projection_k
    return Z


def recover_data(Z, U, K):
    X_rec = np.zeros((len(Z), len(U)))
    for i in range(len(Z)):
        v = Z[i, :]
        for j in range(np.size(U, 1)):
            recovered_j = np.dot(v.T, U[j, 0:K])
            X_rec[i][j] = recovered_j
    return X_rec


def explain_variance(S):
    ########################
    ### SEU CÓDIGO AQUI  ###
    ########################

    # implement code to print the percentages
    # of variation for each dimension.
    pass


def main():
    raw_mat = scipy.io.loadmat("../data/ex7data1.mat")
    X = raw_mat.get("X")
    plt.cla()
    plt.plot(X[:, 0], X[:, 1], 'bo')
    plt.show()

    X_norm, mu, sigma = normalize_features(X)
    U, S = pca(X_norm)

    plt.cla()
    plt.axis('equal')
    plt.plot(X_norm[:, 0], X_norm[:, 1], 'bo')
    plt.show()

    K = 1
    X_proj = project_data(X_norm, U, K)
    print(X_proj[0])

    Z = project_data(X_norm, U, K)
    X_rec = recover_data(Z, U, K)
    print(X_rec[0])

    plt.cla()
    plt.plot(X_norm[:, 0], X_norm[:, 1], 'bo')
    plt.plot(X_rec[:, 0], X_rec[:, 1], 'rx')
    plt.axis('equal')
    plt.show()

    explain_variance(S)


if __name__ == "__main__":
    main()
