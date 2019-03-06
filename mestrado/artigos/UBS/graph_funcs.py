import networkx as nx
import geopy.distance
import collections
import matplotlib.pyplot as plt


def calcula_distancia(cidade_1, cidade_2):
    # Função recebe dois nós e calcula a distância em Km
    # entre eles à partir das coordenadas
    coord1 = (cidade_1['lat'], cidade_1['long'])
    coord2 = (cidade_2['lat'], cidade_2['long'])
    return int(geopy.distance.distance(coord1, coord2).km)


def cria_grafo(df):
    print('Iniciando criação do grafo')
    grafo_ubs = nx.MultiDiGraph()
    grafo_dict = collections.defaultdict(dict)
    for i in range(0, max(df.index) + 1):
        for j in range(0, max(df.index) + 1):
            # Condição para não armazenar um nó com aresta pra si mesmo
            if i != j:
                no1 = df.iloc[i]
                no2 = df.iloc[j]
                # Para cada chave armazena um dicionario com os outros nós
                # (vértices) e a distancia em Km para cada um deles
                grafo_dict[no1['gid']][no2['gid']] = calcula_distancia(no1,
                                                                       no2)
                grafo_ubs.add_edge(no1['gid'], no2['gid'],
                                   weight=calcula_distancia(no1, no2))
    print(grafo_dict)
    print(nx.info(grafo_ubs))
    print('O grafo tem pesos? ' + str(nx.is_weighted(grafo_ubs)))
    # Desenhando o grafo
    print('Desenhando o grafo')
    nx.draw(grafo_ubs, with_labels=True)
    plt.draw()
    plt.show()
