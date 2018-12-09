import pandas as pd
import numpy as np
from graph_funcs import calcula_distancia, cria_grafo, dijkstra, prim
import time
import csv


def main():
    # Caminho e nome dos arquivos de dados
    file_path = r'C:\\Users\\aiqui\\Dropbox\\CEFET\\Disciplinas' \
        r'\\Algoritmos em Grafos\\Trabalho\\Dados\\'
    file_name = 'ubs_funcionamentonone.csv'

    data = pd.read_csv(file_path + file_name, sep=',')
    # Criando um dataset só de dados do RJ
    data_rj = data[data['uf'] == 'RJ']  # 1880 rows
    data_rj = data_rj.reset_index()
    # Criando versão reduzida do dataset pra testes
    timestamps = {}
    for i in range(1, 101):
        start_time = time.time()
        data_rj_reduzido = data_rj[0:i]
        # Cria um grafo com estrutura de dicionário à partir de um
        # Pandas DataFrame. Dicionários são o padrão do Python
        # para representação de grafos
        # Referência: https://www.python.org/doc/essays/graphs/
        grafo = cria_grafo(data_rj_reduzido)
        # Prompt para o usuário selecionar qual problema gostaria de resolver
        # Problema 1 - Menor distância entre duas UBS (com opçaõ de remoção)
        # O problema 1 é um problema de caminhos mínimos
        # Problema 2 - Menos distância para se percorrer todas as UBS
        # O problema 2 é um problema de Árvore Geradora Mínima
        # teste bom: (179, 152) = 75 distancia
        # print('iniciando caminho mínimo')
        # caminho_minimo, distancia_minima = dijkstra(grafo, 179, 152)
        # print('Caminho mínimo = ', caminho_minimo, ' com distância de: ',
        #       distancia_minima, 'Km')
        # print('iniciando prim')
        # prim(grafo)
        timestamps[i] = time.time() - start_time
        with open(r'C:\Users\aiqui\Dropbox\CEFET\Disciplinas\Algoritmos em Grafos\Trabalho\timestamps_cria_grafo_rjfull.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in timestamps.items():
                writer.writerow([key, value])


if __name__ == "__main__":
    main()
