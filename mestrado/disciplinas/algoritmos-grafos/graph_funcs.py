import geopy.distance
import collections


def calcula_distancia(cidade_1, cidade_2):
    # Função recebe dois nós e calcula a distância em Km
    # entre eles à partir das coordenadas
    coord1 = (cidade_1['lat'], cidade_1['long'])
    coord2 = (cidade_2['lat'], cidade_2['long'])
    return int(geopy.distance.distance(coord1, coord2).km)


def cria_grafo(df):
    # Utilizaremos a estrutura defaultdict que facilita
    # a criação de dicionários encadeados
    # Docs: https://docs.python.org/2/library/collections.html#collections.defaultdict # noqa
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
    # Retorna um dicionário ao invés de um defaultdict
    return dict(grafo_dict)


def dijkstra(grafo, inicio, fim, visitado=[], distancias={},
             antecessores={}):
    # Referência: http://www.gilles-bertrand.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html # noqa
    # Testes básicos
    if not grafo:
        print('Grafo vazio')
    if inicio not in grafo:
        print('Vértice inicial não encontrado no grafo')
    if fim not in grafo:
        print('Vértice final não encontrado no grafo')
    # Condição de parada do algoritmo
    if inicio == fim:
        caminho_minimo = []
        pred = fim
        while pred is not None:
            caminho_minimo.append(pred)
            pred = antecessores.get(pred, None)
        print(caminho_minimo)
        return caminho_minimo, distancias[fim]
    else:
        if not distancias:
            distancias[inicio] = 0
        for vizinho in grafo[inicio]:
            if vizinho not in visitado:
                nova_dist = distancias[inicio] + grafo[inicio][vizinho]
                if nova_dist < distancias.get(vizinho, float('inf')):
                    distancias[vizinho] = nova_dist
                    antecessores[vizinho] = inicio
        visitado.append(inicio)
        nao_visitado = {}
        for k in grafo:
            if k not in visitado:
                nao_visitado[k] = distancias.get(k, float('inf'))
        novo_vertice = min(nao_visitado, key=nao_visitado.get)
        return dijkstra(grafo, novo_vertice, fim, visitado, distancias,
                        antecessores)
