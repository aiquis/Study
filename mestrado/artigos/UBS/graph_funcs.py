import networkx as nx
import collections
import matplotlib.pyplot as plt
from maps_funcs import calcula_distancia_gmaps, calcula_distancia_bing
import pandas as pd


def cria_grafo_networkx(df):
    print('Iniciando criação do grafo')
    grafo_ubs = nx.MultiDiGraph()
    for index, row in df.iterrows():
        grafo_ubs.add_edge(row['origem'], row['destino'],
                           weight=row['distancia'])
    print(nx.info(grafo_ubs))
    print('O grafo tem pesos? ' + str(nx.is_weighted(grafo_ubs)))
    return grafo_ubs


def desenha_grafo(grafo):
    # Desenhando o grafo com Matplotlib
    print('Desenhando o grafo com Matplotlib')
    nx.draw_networkx(grafo, with_labels=True)
    plt.draw()
    plt.show()
    # Desenhando o grafo com pygraphviz
    # print('Desenhando o grafo com pygraphviz')
    # graphviz = nx.nx_agraph.to_agraph(grafo)
    # graphviz.draw('D:\\repos\\study\\mestrado\\artigos\\UBS\\grafo.png')


def cria_instancia_grafo(df, file_name):
    # Criando o arquivo de dados
    file = 'D:\\repos\\study\\mestrado\\artigos\\UBS\\instancias\\%s' \
        % file_name
    print(file)
    f = open(file, 'w+')
    # Qtd de nós do grafo é a qtd de linhas do DataFrame
    qtd_nos = len(df.index)
    # Qtd de arestas do grafo é multiplicada por 2 pois
    # existem nós nos dois sentidos
    qtd_arestas = int((qtd_nos * ((qtd_nos - 1) / 2)) * 2)
    # Escrevendo no arquivo a qtd_nos e qtd_arestas como 1a linha
    f.write(str(qtd_nos) + '\t' + str(qtd_arestas) + '\n')
    # Escrevendo no arquivo as coordenadas de cada registro do DataFrame
    for index, row in df.iterrows():
        print('row: ', row)
        f.write(str(row['lat_corrigida']) + '\t' +
                str(row['long_corrigida']) + '\n')
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
                        '\t' + str(calcula_distancia_bing(no1, no2)) + '\n')
    f.close()


def roda_funcoes_grafo(nx_grafo):
    # Connectivity (em "Approximations and Heuristics")
    print('Connectivity')
    print(nx.all_pairs_node_connectivity(nx_grafo))
    # Centrality degree (em "Centrality")
    print('Centrality degree')
    print(nx.degree_centrality(nx_grafo))
    # Closeness (em "Centrality")
    print('Closeness')
    print(nx.closeness_centrality(nx_grafo, distance='weight'))
    # (Shortest Path) Betweenness (em "Centrality")
    print('Shortest path betweenness')
    print(nx.betweenness_centrality(nx_grafo, normalized=False,
          weight='weight'))
    # Communicability Betweenness
    print('Communicability Betweenness')
    print(nx.communicability_betweenness_centrality(nx_grafo.to_undirected(),
          normalized=False))


def roda_shortest_path_mst(nx_grafo, file_name_prefix):
    # Função para execução de funções de grafos voltadas
    # para a escrita do artigo. Foco em caminhos minímos,
    # otimizações de distâncias, e Árvore Geradora Mínima

    # Executando função para pegar os caminhos mínimos de todos
    # os nós para todos os outros
    lista_dijkstra_path = []
    dijkstra_dict_path = dict(nx.all_pairs_dijkstra_path(nx_grafo,
                                                         weight='weight'))
    for key, value in dijkstra_dict_path.items():
        for key2, value2 in value.items():
            lista_dijkstra_path.append([key, key2, value2])
    dijkstra_df_path = pd.DataFrame(lista_dijkstra_path,
                                    columns=['origem', 'destino', 'caminho'])
    dijkstra_df_path.to_csv('D:\\repos\\study\\mestrado\\artigos\\UBS\\resultados\\' +
                            str(file_name_prefix) + '_dijkstra_path.csv',
                            sep=';')

    # Executando função para pegar as distâncias dos caminhos
    # mínimos entre todos os nós
    lista_dijkstra_length = []
    dijkstra_dict_length = dict(nx.all_pairs_dijkstra_path_length(
        nx_grafo, weight='weight'))
    for key, value in dijkstra_dict_length.items():
        for key2, value2 in value.items():
            lista_dijkstra_length.append([key, key2, value2])
    dijkstra_df_length = pd.DataFrame(lista_dijkstra_length,
                                      columns=['origem',
                                               'destino',
                                               'distancia'])
    # Arredondando valores das distâncias para duas casas decimais
    dijkstra_df_length = dijkstra_df_length.round(2)
    dijkstra_df_length.to_csv('D:\\repos\\study\\mestrado\\artigos\\UBS\\resultados\\' +
                              str(file_name_prefix) + '_dijkstra_length.csv',
                              sep=';')

    # Cálculo da média dos caminhos mínimos. Com isso podemos saber
    # por exemplo a distância mínima que um paciente terá que percorrer
    # em média para ir para uma outra UBS
    average_shortest_path = nx.average_shortest_path_length(nx_grafo,
                                                            weight='weight')
    print('Average Shortest Path: ', average_shortest_path)

    # Executando Árvore Geradora Mínima do Grafo
    # O algoritmo traz o caminho e distância para percorrer
    # todos os nós do grafo
    mst_list = []
    mst = nx.minimum_spanning_tree(nx_grafo.to_undirected(), weight='weight')
    for i, o, w in nx_grafo.edges(data=True):
        if ((i, o) in mst.edges() or (o, i) in mst.edges()):
            mst_list.append([i, o, w])
    mst_df = pd.DataFrame(mst_list, columns=['de', 'para', 'distancia'])
    mst_df.to_csv('D:\\repos\\study\\mestrado\\artigos\\UBS\\resultados\\' +
                  str(file_name_prefix) + '_mst.csv',
                  sep=';')


def roda_funcoes_centralidade(nx_grafo, file_name_prefix):
    # Função para execução de algoritmos de centralidade de grafos
    # São executados os seguintes algoritmos:
    # Closeness Centrality, Betweenness Centrality e Efficiency Centrality
    # Os resultados das execuções são gravados em um arquivo .txt

    # Closeness Centrality
    print('Executando algoritmo de Closeness Centrality')
    closeness = nx.closeness_centrality(nx_grafo, distance='weight')

    # Betweenness Centrality
    print('Executando algoritmo de Betweenness Centrality')
    betweenness = nx.betweenness_centrality(nx_grafo, normalized=False, weight='weight')

    # Centrality degree
    print('Executando algoritmo de Centrality degree')
    degree_centrality = nx.degree_centrality(nx_grafo)

    # Efficiency Centrality
    print('Executando algoritmo de Global Efficiency')
    efficiency = nx.global_efficiency(nx.to_undirected(nx_grafo))

    # Abrindo arquivo texto para gravação dos resultados
    file = 'D:\\repos\\study\\mestrado\\artigos\\UBS\\resultados\\%s' \
        % str(file_name_prefix) + '_centralidade.txt'
    print(file)
    f = open(file, 'w+')
    f.write('Closeness Centrality' + '\n')
    f.write(str(closeness) + '\n')
    f.write('Betweenness Centrality' + '\n')
    f.write(str(betweenness) + '\n')
    f.write('Degree Centrality' + '\n')
    f.write(str(degree_centrality) + '\n')
    f.write('Efficiciency Centrality' + '\n')
    f.write(str(efficiency))
    f.close()


def calculo_centro_grafo(nx_grafo):
    # Função para calcular o centro do grafo e o menor caminho
    # dele para todos os outros nós do grafo

    # Calculo do centro do grafo
    lista_centro_grafo = nx.center(nx_grafo)
    print('Nós centrais do grafo: ', lista_centro_grafo)


def elimina_arestas(nx_grafo, distancia_max):
    grafo_incompleto = nx.Graph([(u, v, d) for u, v, d
                                in nx_grafo.edges(data=True)
                                if d['weight'] < distancia_max])
    print(nx.info(grafo_incompleto))
    print('O grafo tem pesos? ' + str(nx.is_weighted(grafo_incompleto)))
    return grafo_incompleto


def caminhos_minimos_um_no(nx_grafo, no, file_name_prefix):
    lista_dijkstra_path = []
    dijkstra_dict_path = dict(nx.single_source_dijkstra_path(nx_grafo, no,
                                                             weight='weight'))
    for key, value in dijkstra_dict_path.items():
        lista_dijkstra_path.append([no, key, value])
    dijkstra_df_path = pd.DataFrame(lista_dijkstra_path,
                                    columns=['origem', 'destino', 'caminho'])
    dijkstra_df_path.to_csv('D:\\repos\\study\\mestrado\\artigos\\UBS\\resultados\\' +
                            str(file_name_prefix) + str(no) +
                            '_dijkstra_path_singlesource.csv',
                            sep=';')

    # Executando função para pegar as distâncias dos caminhos
    # mínimos entre todos os nós
    lista_dijkstra_length = []
    dijkstra_dict_length = dict(nx.single_source_dijkstra_path_length(
        nx_grafo, no, weight='weight'))
    for key, value in dijkstra_dict_length.items():
        lista_dijkstra_length.append([no, key, value])
    dijkstra_df_length = pd.DataFrame(lista_dijkstra_length,
                                      columns=['origem',
                                               'destino',
                                               'distancia'])
    # Arredondando valores das distâncias para duas casas decimais
    dijkstra_df_length = dijkstra_df_length.round(2)
    dijkstra_df_length.to_csv('D:\\repos\\study\\mestrado\\artigos\\UBS\\resultados\\' +
                              str(file_name_prefix) + str(no) +
                              '_dijkstra_length_singlesource.csv',
                              sep=';')
