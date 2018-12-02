import collections


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
        return caminho_minimo, distancias[fim]
    else:
        if not distancias:
            distancias[inicio] = 0
        for vizinho in grafo[inicio]:
            print('vizinho de ', inicio, ' analisado = ', vizinho)
            if vizinho not in visitado:
                nova_dist = distancias[inicio] + grafo[inicio][vizinho]
                print('nova_dist: ', nova_dist)
                if nova_dist < distancias.get(vizinho, float('inf')):
                    distancias[vizinho] = nova_dist
                    antecessores[vizinho] = inicio
                    print('distancias: ', distancias)
                    print('antecessores: ', antecessores)
        visitado.append(inicio)
        print('visitado: ', visitado)
        nao_visitado = {}
        for k in grafo:
            print('k: ', k)
            if k not in visitado:
                nao_visitado[k] = distancias.get(k, float('inf'))
                print('Não visitados: ', nao_visitado)
        novo_vertice = min(nao_visitado, key=nao_visitado.get)
        print('Novo vértice a ser explorado: ', novo_vertice)
        return dijkstra(grafo, novo_vertice, fim, visitado, distancias,
                        antecessores)
