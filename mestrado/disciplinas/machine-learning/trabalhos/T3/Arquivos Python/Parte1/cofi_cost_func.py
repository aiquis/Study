import numpy as np


def cofi_cost_func(params, Y, R, num_users, num_movies, num_features, Lambda):
    # Y: num_movies x num_users: matriz de classificação de filmes por usuários
    # R: num_movies x num_users: matriz, onde R (i, j) = 1 se o i-ésimo filme
    # foi avaliado pelo j-ésimo usuário
    # Obtém as matrizes X e Theta a partir dos params
    # X: num_movies x num_features: matriz de features dos filmes
    X = np.array(params[:num_movies * num_features]).reshape(
        num_features, num_movies).T.copy()
    # Theta: num_users x num_features: matriz de features dos usuários
    Theta = np.array(params[num_movies * num_features:]).reshape(
        num_features, num_users).T.copy()

    # Você deve retornar os seguintes valores corretamente
    J = 0
    X_grad = np.zeros(X.shape)
    Theta_grad = np.zeros(Theta.shape)

    # ====================== SEU CÓDIGO AQUI ======================
    # 2.2.1 - Função de custo da filtragem colaborativa
    error = X.dot(Theta.T) - Y
    # Pegando apenas registros de filmes que o usuário avaliou
    error = error * R
    # Sem regularização
    J = 1 / 2 * np.sum(np.square(error))
    # Com regularização
    J += (Lambda / 2) * np.sum(np.square(X)) + (Lambda / 2) * np.sum(
        np.square(Theta))

    # 2.2.2 - Gradiente de filtragem colaborativa
    X_grad = error.dot(Theta)
    Theta_grad = error.T.dot(X)
    # Aplicando regularização
    X_grad += Lambda * X
    Theta_grad += Lambda * Theta

    # ===================== FIM DO MEU CÓDIGO =====================

    grad = np.hstack((X_grad.T.flatten(), Theta_grad.T.flatten()))

    return J, grad
