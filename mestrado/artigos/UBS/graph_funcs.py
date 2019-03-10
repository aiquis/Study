import networkx as nx
import geopy.distance
import collections
import matplotlib.pyplot as plt
import googlemaps


def calcula_distancia_gmaps(cidade_1, cidade_2):
    # Função recebe dois nós e calcula a distância em Km
    # entre eles à partir das coordenadas
    # Preencher API Key da aplicação distancia-ubs
    google_maps_api_key = ''
    gmaps = googlemaps.Client(key=google_maps_api_key)
    coord1 = (cidade_1['lat'], cidade_1['long'])
    coord2 = (cidade_2['lat'], cidade_2['long'])
    distancia = gmaps.distance_matrix(coord1, coord2,
                                      mode='driving')
    distancia = distancia['rows'][0]['elements'][0]['distance']['value']
    print('Coord1: ' + str(coord1))
    print('Coord2: ' + str(coord2))
    print('Distância: ' + str(distancia))
    return distancia


def calcula_distancia(cidade_1, cidade_2):
    # Função recebe dois nós e calcula a distância em Km
    # entre eles à partir das coordenadas
    coord1 = (cidade_1['lat'], cidade_1['long'])
    coord2 = (cidade_2['lat'], cidade_2['long'])
    return int(geopy.distance.distance(coord1, coord2).km)


def cria_grafo_networkx(df):
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
    return grafo_ubs


def desenha_grafo(grafo):
    # Desenhando o grafo com Matplotlib
    print('Desenhando o grafo com Matplotlib')
    nx.draw(grafo, with_labels=True)
    plt.draw()
    plt.show()
    # Desenhando o grafo com pygraphviz
    # print('Desenhando o grafo com pygraphviz')
    # graphviz = nx.nx_agraph.to_agraph(grafo)
    # graphviz.draw('D:\\repos\\study\\mestrado\\artigos\\UBS\\grafo.png')


def cria_instacias_grafos(df):
    # Criando o arquivo de dados
    f = open('D:\\repos\\study\\mestrado\\artigos\\UBS\\instancias'
             '\\arquivos_dados.txt', 'w+')
    # Qtd de nós do grafo é a qtd de linhas do DataFrame
    qtd_nos = len(df.index)
    # Qtd de arestas do grafo é multiplicada por 2 pois
    # existem nós nos dois sentidos
    qtd_arestas = int((qtd_nos * ((qtd_nos - 1) / 2)) * 2)
    # Escrevendo no arquivo a qtd_nos e qtd_arestas como 1a linha
    f.write(str(qtd_nos) + '\t' + str(qtd_arestas) + '\n')
    # Escrevendo no arquivo as coordenadas de cada registro do DataFrame
    for index, row in df.iterrows():
        f.write(str(row['lat']) + '\t' + str(row['long']) + '\n')
    # Escrevendo no arquivo as distânciasentre cada
    for i in range(0, max(df.index) + 1):
        for j in range(0, max(df.index) + 1):
            # Condição para não armazenar um nó com aresta pra si mesmo
            if i != j:
                no1 = df.iloc[i]
                no2 = df.iloc[j]
                # Para cada chave armazena um dicionario com os outros nós
                # (vértices) e a distancia em Km para cada um deles
                f.write(str(no1['gid']) + '\t' + str(no2['gid']) +
                        '\t' + str(calcula_distancia(no1, no2)) + '\n')
    f.close()
