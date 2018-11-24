import numpy as np
import matplotlib.pyplot as plt

"""
Paralell K-means definition

The N points are partitioned among the parallel tasks
and each parallel processes read the K initial centroids.
After this step, every task calculates is nearest centroid
for each point. The local avarage of these points for each
centroid is used in a global avarage to get the new
centroids position.
"""


def find_closest_centroids(X, centroids):
    # Tive que fazer uma correção nessa primeira linha pois o código
    # trazia K = 2 ao invés de K = 3
    K = centroids.shape[0]
    idx = np.zeros((len(X), 1), dtype=np.int8)

    for i in range(len(idx)):
        # Definindo um limite alto para min_dist para garantir
        # que ele vá ser maior que a primeira distância euclisiana
        # calculada entre um ponto e a localização do centroid
        min_dist = 1000000
        for j in range(K):
            # Calculando a distância euclisiana dos dados até os centroides
            dist = np.sqrt(np.sum((X[i, :] - centroids[j, :]) ** 2))
            if dist < min_dist:
                # Definindo a qual cluster cada observação pertence
                min_dist = dist
                # Atribuindo a qual cluster K cada observação
                # em X pertence
                idx[i] = j
    return idx


def compute_centroids(X, idx, K):
    centroids = np.zeros((K, np.size(X, 1)))
    # Para cada K, vamos definir um novo valor dos centróides dentro do loop
    for i in range(K):
        # aux recebe todos os valores de idx equivalentes aos agrupamento i
        aux = np.where(idx == i)[0]
        # Calcula a média dos valores daquele agrupamento para gerar
        # o novo centróide
        centroids[i, :] = np.mean(X[aux, :], axis=0)
    return centroids


def kmeans_init_centroids(X, K):
    return X[np.random.choice(X.shape[0], K, replace=False)]


def run_kmeans(X, initial_centroids, max_iters, plot_progress=False):
    K = np.size(initial_centroids, 0)
    centroids = initial_centroids
    previous_centroids = centroids

    # Parte dentro desse for que será paralelizada
    for iter in range(max_iters):
        # Assignment of examples do centroids
        idx = find_closest_centroids(X, centroids)

        # PLot the evolution in centroids through the iterations
        if plot_progress:
            plt.scatter(X[np.where(idx == 0), 0],
                        X[np.where(idx == 0), 1], marker='x')
            plt.scatter(X[np.where(idx == 1), 0],
                        X[np.where(idx == 1), 1], marker='x')
            plt.scatter(X[np.where(idx == 2), 0],
                        X[np.where(idx == 2), 1], marker='x')
            plt.plot(previous_centroids[:, 0], previous_centroids[:, 1],
                     'yo')
            plt.plot(centroids[:, 0], centroids[:, 1], 'bo')
            plt.show()

        previous_centroids = centroids

        # Aqui a paralelização "termina", juntando os resultados
        # para gerar o novo conjunto de centroids
        # Compute new centroids
        centroids = compute_centroids(X, idx, K)

    return (centroids, idx)
