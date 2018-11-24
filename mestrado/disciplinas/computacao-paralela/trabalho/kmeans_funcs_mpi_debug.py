import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI


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
    print('Vetor recebido', X)
    # Tive que fazer uma correção nessa primeira linha pois o código
    # trazia K = 2 ao invés de K = 3
    K = centroids.shape[0]
    idx = np.zeros((len(X), 1), dtype=np.int8)
    print('idx shape: ', idx.shape)
    print('centroids shape: ', centroids.shape)

    for i in range(len(idx)):
        print('Iniciando loop com i')
        # Definindo um limite alto para min_dist para garantir
        # que ele vá ser maior que a primeira distância euclisiana
        # calculada entre um ponto e a localização do centroid
        min_dist = 1000000
        for j in range(K):
            print('Iniciando loop com J')
            # Calculando a distância euclisiana dos dados até os centroides
            dist = np.sqrt(np.sum((X[i, :] - centroids[j, :]) ** 2))
            print('dist: ', dist)
            if dist < min_dist:
                # Definindo a qual cluster cada observação pertence
                min_dist = dist
                idx[i] = j
    print('Fim do find_closest_centroids. Retornando idx', idx)
    return idx


def compute_centroids(X, idx, K):
    centroids = np.zeros((K, np.size(X, 1)))
    print('centroids shape (compute): ', centroids.shape)
    # Para cada K, vamos definir um novo valor dos centróides dentro do loop
    for i in range(K):
        print('i: ', i)
        # aux recebe todos os valores de idx equivalentes aos agrupamento i
        aux = np.where(idx == i)[0]
        # Calcula a média dos valores daquele agrupamento para gerar
        # o novo centróide
        print('centroids[i, :]: ', centroids[i, :])
        print('X[aux, :]: ', X[aux, :])
        centroids[i, :] = np.mean(X[aux, :], axis=0)
    return centroids


def kmeans_init_centroids(X, K):
    return X[np.random.choice(X.shape[0], K, replace=False)]


def run_kmeans(X, initial_centroids, max_iters, comm, plot_progress=False):
    rank = comm.Get_rank()
    size = comm.Get_size()
    print('X.size: ', X.size)
    print('len(X)', len(X))
    recvdata = np.empty((int(len(X) / size), X.shape[1]), dtype=np.float64)
    if rank == 0:
        senddata = X
        print('Vamos fazer scatter de: ', senddata)
    else:
        senddata = None
    comm.Scatter(senddata, recvdata, root=0)
    print('No processo: ', rank, 'temos os dados: ', recvdata)
    K = np.size(initial_centroids, 0)
    centroids = initial_centroids
    previous_centroids = centroids

    # Parte dentro desse for que será paralelizada
    for iter in range(max_iters):
        # Assignment of examples do centroids
        print('recvdata enviado pro find_closest_centroid:', recvdata.shape)
        idx = find_closest_centroids(recvdata, centroids)

        # PLot the evolution in centroids through the iterations
        """
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
        """
        # Iniciando processo de Gather dos dados e centroids
        if rank == 0:
            data_gathered = np.empty(X.shape, dtype=np.float64)
            idx_gathered = np.empty((X.shape[0], 1), dtype=np.int8)
            print('data_gathered shape: ', data_gathered.shape)
            print('idx_gathered shape: ', idx_gathered.shape)
        else:
            data_gathered = None
            idx_gathered = None
        
        print('Iniciando Gather dos dados')
        comm.Gather(recvdata, data_gathered, root=0)
        print('data_gathered: ', data_gathered)
        comm.Gather(idx, idx_gathered, root=0)
        print('idx_gathered: ', idx_gathered)

        if rank == 0:
            previous_centroids = centroids
            # Aqui a paralelização "termina", juntando os resultados
            # para gerar o novo conjunto de centroids
            # Compute new centroids
            print("Chamando função compute_centroids")
            centroids = compute_centroids(data_gathered, idx_gathered, K)

    return (centroids, idx_gathered)
