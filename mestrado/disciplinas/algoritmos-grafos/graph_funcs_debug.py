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

def prim(grafo):
    agm_custo = 0
    agm_vertices = []
    vertices = {}
    # Criando chaves para cada vértice do grafo de entrada
    for i in grafo:
        if not vertices:
            # 0 para o primeiro elemento para ser o primeiro
            vertices[i] = 0
        else:
            # Inicializando todos os outros vérticos com infinito
            # pois ainda não sabemos suas distâncias
            vertices[i] = float('inf')
    print(vertices)
    # Condição de parada = todos os vértices do grafo estarem em agm_vertices
    visitar_no = min(vertices, key=vertices.get)
    todos_vertices = False
    while not todos_vertices:
        if ((visitar_no in vertices) and (visitar_no not in agm_vertices)):
            agm_vertices.append(visitar_no)
            print('agm_vertices: ', agm_vertices)
            vizinhos = grafo.get(visitar_no)
            for key, value in vizinhos.items():
                if vertices[key] > value:
                    vertices[key] = value
            print('Vertices: ', vertices)
            menor_peso = float('inf')
            for key, value in vertices.items():
                print('key: ', key)
                if key not in agm_vertices:
                    print('value: ', value)
                    if value < menor_peso:
                        menor_peso = value
                        print('Menor peso: ', menor_peso)
                        visitar_no = key
            agm_custo += menor_peso
            print('agm_custo: ', agm_custo)
            print('proximo a visitar: ', visitar_no)
        else:
            print('entrou no else')
            todos_vertices = True
    print('Árvore Geradora Mínima: ', agm_vertices)
    print('Custo total: ', agm_custo)
    return None
