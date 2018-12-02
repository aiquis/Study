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
        # Inicialização das distâncias para primeira execução
        if not distancias:
            distancias[inicio] = 0
        # Busca os vizinhos do vértice ainda não visitados e atualiza
        # as distâncias para cada vértice caso o custo melhore
        for vizinho in grafo[inicio]:
            if vizinho not in visitado:
                nova_dist = distancias[inicio] + grafo[inicio][vizinho]
                if nova_dist < distancias.get(vizinho, float('inf')):
                    distancias[vizinho] = nova_dist
                    antecessores[vizinho] = inicio
        # Atualiza os vértices já visitados
        visitado.append(inicio)
        nao_visitado = {}
        # Busca todos os vértices ainda não visitados e seleciona
        # o com menor custo para ser o próximo a visitar
        for k in grafo:
            if k not in visitado:
                nao_visitado[k] = distancias.get(k, float('inf'))
        novo_vertice = min(nao_visitado, key=nao_visitado.get)
        # Chama a função recursovamente com o novo inicio (que é o
        # vértice com menor custo selecionado anteriormente)
        # Passa também as listas de vértices visitados, menores distâncias
        # e antecessores atualizada
        return dijkstra(grafo, novo_vertice, fim, visitado, distancias,
                        antecessores)


def prim(grafo):
    # Inicialização de variáveis
    agm_custo = 0
    agm_vertices = []
    vertices = {}
    iteracoes = 0
    # Criando chaves para cada vértice do grafo de entrada
    for i in grafo:
        if not vertices:
            # 0 para o primeiro elemento para ser o primeiro
            # Poderia selecionar aleatoriamente também
            vertices[i] = 0
        else:
            # Inicializando todos os outros vérticos com infinito
            # pois ainda não sabemos suas distâncias
            vertices[i] = float('inf')
    # Obtendo nó inicializado com custo 0 como ponto de partida
    # do algoritmo e um booleano que controla uma das
    # condições de parada
    visitar_no = min(vertices, key=vertices.get)
    todos_vertices = False
    # Condição de parada = todos os vértices do grafo estarem em agm_vertices
    # e agm_vertices ter vertices - 1 elementos
    while (not todos_vertices and len(agm_vertices) < len(vertices) - 1):
        iteracoes += 1
        print('Iteração ', iteracoes)
        # Para se elegível o nó não pode já ter sido visitado, ou seja,
        # estar na lista agm_vertices
        if ((visitar_no in vertices) and (visitar_no not in agm_vertices)):
            # Adiciona o nó a lista de nós já no caminho
            # Busca seus vizinhos e atualiza os custos para cada vértice
            # Caso o custo nesse nó para atingir o outro seja menor do que
            # o custo já armazenado
            agm_vertices.append(visitar_no)
            vizinhos = grafo.get(visitar_no)
            for key, value in vizinhos.items():
                if vertices[key] > value:
                    vertices[key] = value
            # Encontra o vértice adjacente com menor custo para ser o
            # próximo a ser explorado
            menor_peso = float('inf')
            for key, value in vertices.items():
                if key not in agm_vertices:
                    if value < menor_peso:
                        menor_peso = value
                        visitar_no = key
            print('Inserindo o no', visitar_no, 'com peso', menor_peso)
            # Soma do custo da Árvore Geradora Mínima
            agm_custo += menor_peso
        else:
            # Quando a condição de parada for atingida altera o booleano
            # e print a Árvore gerado e seu custo total
            todos_vertices = True
    print('Árvore Geradora Mínima: ', agm_vertices)
    print('Custo total (em Km): ', agm_custo)
    return None
