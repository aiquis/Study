import numpy as np
import scipy.io
import matplotlib.pyplot as plt


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

        # Compute new centroids
        centroids = compute_centroids(X, idx, K)

    return (centroids, idx)


def main():
    # Find closest centroids
    raw_mat = scipy.io.loadmat("../data/ex7data2.mat")
    X = raw_mat.get("X")

    K = 3

    # Fixed seeds (i.e., initial centroids)
    initial_centroids = np.array([[3, 3], [6, 2], [8, 5]])
    idx = find_closest_centroids(X, initial_centroids)

    # Plot initial assignments.
    plt.scatter(X[np.where(idx == 0), 0], X[np.where(idx == 0), 1], marker='x')
    plt.scatter(X[np.where(idx == 1), 0], X[np.where(idx == 1), 1], marker='x')
    plt.scatter(X[np.where(idx == 2), 0], X[np.where(idx == 2), 1], marker='x')
    plt.title('Initial assignments')
    plt.show()

    print('Cluster assignments for the first, '
          'second and third examples: ' + str(idx[0:3].flatten()))

    # Compute initial means
    centroids = compute_centroids(X, idx, K)

    # Now run 10 iterations of K-means on fixed seeds
    initial_centroids = np.array([[3, 3], [6, 2], [8, 5]])
    # initial_centroids = kmeans_init_centroids(X, K)
    max_iters = 10
    centroids, idx = run_kmeans(X, initial_centroids, max_iters,
                                plot_progress=False)
    print('Centroids after the 1st update:\n' + str(centroids))

    # Plot final clustering.
    plt.scatter(X[np.where(idx == 0), 0], X[np.where(idx == 0), 1], marker='x')
    plt.scatter(X[np.where(idx == 1), 0], X[np.where(idx == 1), 1], marker='x')
    plt.scatter(X[np.where(idx == 2), 0], X[np.where(idx == 2), 1], marker='x')
    plt.title('Final clustering')
    plt.show()

    initial_centroids = kmeans_init_centroids(X, K)
    idx = find_closest_centroids(X, initial_centroids)

    # Plot initial assignments.
    plt.scatter(X[np.where(idx == 0), 0], X[np.where(idx == 0), 1], marker='x')
    plt.scatter(X[np.where(idx == 1), 0], X[np.where(idx == 1), 1], marker='x')
    plt.scatter(X[np.where(idx == 2), 0], X[np.where(idx == 2), 1], marker='x')
    plt.title('Initial assignments')
    plt.show()

    print('Cluster assignments for the first, '
          'second and third examples: ' + str(idx[0:3].flatten()))

    # Compute initial means
    centroids = compute_centroids(X, idx, K)

    # Now run 10 iterations of K-means on fixed seeds
    initial_centroids = np.array([[3, 3], [6, 2], [8, 5]])
    # initial_centroids = kmeans_init_centroids(X, K)
    max_iters = 10
    centroids, idx = run_kmeans(X, initial_centroids, max_iters,
                                plot_progress=False)
    print('Centroids after the 1st update:\n' + str(centroids))

    # Plot final clustering.
    plt.scatter(X[np.where(idx == 0), 0], X[np.where(idx == 0), 1], marker='x')
    plt.scatter(X[np.where(idx == 1), 0], X[np.where(idx == 1), 1], marker='x')
    plt.scatter(X[np.where(idx == 2), 0], X[np.where(idx == 2), 1], marker='x')
    plt.title('Final clustering')
    plt.show()


if __name__ == "__main__":
    main()
