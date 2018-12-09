import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
# Para execução sequencial alterar o import para kmeans_funcs
from kmeans_funcs_mpi import (find_closest_centroids,
                              compute_centroids,
                              kmeans_init_centroids,
                              run_kmeans)
from mpi4py import MPI
import time
import csv


def read_file(file_path, file_name, num_rows):
    dataset = pd.read_csv(file_path+file_name, sep=',', nrows=num_rows)
    return dataset


def preprocess_features(dataset):
    scaler = MinMaxScaler(copy=False)
    dataset = scaler.fit_transform(dataset)
    return dataset


def main():
    file_path = '/home/aiquis/datasets/census1990-mld/'
    file_name = 'USCensus1990.data.txt'
    # Altere essa variável para determinar número de observações
    # a serem lidas do dataset do Censo
    num_rows = 50000
    # Descomentar o código abaixo para execução do dataset do Censo
    """
    X = read_file(file_path, file_name, num_rows)
    X.drop('caseid', axis=1, inplace=True)
    X = np.array(X)
    X = preprocess_features(X)
    """
    # Criando dataset randômico com seed para manter reproducibilidade
    # Caso deseja executar o dataset do Censo, descomentar o trecho de
    # código sinalizado acima e comentar as duas linhas abaixo
    np.random.seed(0)
    X = np.random.rand(50000, 2)
    # Inicializando dicionário para armazenar tempos de execução
    timestamps = {}
    for i in range(1, 101):
        # start_time recebe momento de inicio da execução de cada
        # iteração do loop
        start_time = time.time()
        # Quantidade de cluster varia para as iterações do loop
        K = i

        # "Each parallel processes read the K initial centroids"
        # initial_centroids = kmeans_init_centroids(X, K)
        # "Every task calculates its nearest centroid for each point"
        # idx = find_closest_centroids(X, initial_centroids)

        # Inicialização do conjunto de centroides inicial
        initial_centroids = kmeans_init_centroids(X, K)

        # Inicio da execução paralela com MPI
        # Para execução sequencial comentar essa linha
        comm = MPI.COMM_WORLD
        # Define número de iterações do algoritmo
        max_iters = 5
        # Execução do K-means
        centroids, idx = run_kmeans(X, initial_centroids, max_iters,
                                    comm)
        # Trecho comentado que exibe plot das execuções do K-means
        """
        # Plot final clustering.
        plt.scatter(X[np.where(idx == 0), 0], X[np.where(idx == 0), 1], marker='x')
        plt.scatter(X[np.where(idx == 1), 0], X[np.where(idx == 1), 1], marker='x')
        plt.scatter(X[np.where(idx == 2), 0], X[np.where(idx == 2), 1], marker='x')
        plt.scatter(X[np.where(idx == 3), 0], X[np.where(idx == 3), 1], marker='x')
        plt.scatter(X[np.where(idx == 4), 0], X[np.where(idx == 4), 1], marker='x')
        plt.scatter(X[np.where(idx == 5), 0], X[np.where(idx == 5), 1], marker='x')
        plt.scatter(X[np.where(idx == 6), 0], X[np.where(idx == 6), 1], marker='x')
        plt.scatter(X[np.where(idx == 7), 0], X[np.where(idx == 7), 1], marker='x')
        plt.scatter(X[np.where(idx == 8), 0], X[np.where(idx == 8), 1], marker='x')
        plt.scatter(X[np.where(idx == 9), 0], X[np.where(idx == 9), 1], marker='x')
        plt.scatter(X[np.where(idx == 10), 0], X[np.where(idx == 10), 1], marker='x')
        plt.title('Final clustering')
        plt.show()
        """
        # Gravando tempo de execução da iteração para K = i
        timestamps[i] = time.time() - start_time
    # Escrevendo os timestamps num CSV
    with open('/home/aiquis/timestamps_k100.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in timestamps.items():
            writer.writerow([key, value])


if __name__ == '__main__':
    main()
