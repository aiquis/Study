import pandas as pd
from graph_funcs import cria_instancia_grafo
from maps_funcs import get_coordenadas


def cria_instancias(data):
    # Criação de dataset pra UBSs do estado do RJ
    data_estado_rj = data[data['uf'] == 'RJ']
    data_estado_rj.reset_index(inplace=True)
    grava_arquivo(data_estado_rj, 'data_estado_rj.csv')
    # cria_instancia_grafo(data_estado_rj, 'grafo_estado_rj.txt')

    # Criação de dataset pra UBSs do estado do SP
    data_estado_sp = data[data['uf'] == 'SP']
    data_estado_sp.reset_index(inplace=True)
    grava_arquivo(data_estado_sp, 'data_estado_sp.csv')
    # cria_instancia_grafo(data_estado_sp, 'grafo_estado_sp.txt')

    # Criação de dataset para UBSs do estado de MG
    data_estado_mg = data[data['uf'] == 'MG']
    data_estado_mg.reset_index(inplace=True)
    grava_arquivo(data_estado_mg, 'data_estado_mg.csv')
    # cria_instancia_grafo(data_estado_mg, 'grafo_estado_mg.txt')

    # Criação de dataset pra cidade do RJ
    data_cidade_rio = data[(data['uf'] == 'RJ') &
                           (data['cidade'] == 'Rio de Janeiro')]
    data_cidade_rio.reset_index(inplace=True)
    grava_arquivo(data_cidade_rio, 'data_cidade_rio.csv')
    # cria_instancia_grafo(data_cidade_rio, 'grafo_cidade_rio.txt')

    # Criação de dataset pra cidade de SP
    data_cidade_saopaulo = data[(data['uf'] == 'SP') &
                                (data['cidade'] == 'São Paulo')]
    data_cidade_saopaulo.reset_index(inplace=True)
    grava_arquivo(data_cidade_saopaulo, 'data_cidade_saopaulo.csv')
    # cria_instancia_grafo(data_cidade_saopaulo, 'grafo_cidade_saopaulo.txt')

    # Criação de dataset pra região sudeste
    data_regiao_sudeste = data[(data['uf'] == 'RJ') | (data['uf'] == 'SP') |
                               (data['uf'] == 'MG') | (data['uf'] == 'ES')]
    data_regiao_sudeste.reset_index(inplace=True)
    grava_arquivo(data_regiao_sudeste, 'data_regiao_sudeste.csv')
    # cria_instancia_grafo(data_regiao_sudeste, 'grafo_regiao_sudeste.txt')

    # Criação de dataset para região sul
    data_regiao_sul = data[(data['uf'] == 'PR') | (data['uf'] == 'SC') |
                           (data['uf'] == 'RS')]
    data_regiao_sul.reset_index(inplace=True)
    grava_arquivo(data_regiao_sul, 'data_regiao_sul.csv')
    # cria_instancia_grafo(data_regiao_sul, 'grafo_regiao_sul.txt')

    # Criação de dataset para região nordeste
    data_regiao_nordeste = data[(data['uf'] == 'BA') | (data['uf'] == 'SE') |
                                (data['uf'] == 'AL') | (data['uf'] == 'PE') |
                                (data['uf'] == 'PE') | (data['uf'] == 'PB') |
                                (data['uf'] == 'RN') | (data['uf'] == 'CE') |
                                (data['uf'] == 'PI') | (data['uf'] == 'MA')]
    data_regiao_nordeste.reset_index(inplace=True)
    grava_arquivo(data_regiao_nordeste, 'data_regiao_nordeste.csv')
    # cria_instancia_grafo(data_regiao_nordeste, 'grafo_regiao_nordeste.txt')

    # Criação de dataset para região norte
    data_regiao_norte = data[(data['uf'] == 'TO') | (data['uf'] == 'PA') |
                             (data['uf'] == 'AP') | (data['uf'] == 'RR') |
                             (data['uf'] == 'AM') | (data['uf'] == 'RO') |
                             (data['uf'] == 'AC')]
    grava_arquivo(data_regiao_norte, 'data_regiao_norte.csv')
    # cria_instancia_grafo(data_regiao_norte, 'grafo_regiao_norte.txt')

    return (data_estado_rj, data_estado_sp, data_estado_mg, data_cidade_rio,
            data_cidade_saopaulo, data_regiao_sudeste, data_regiao_sul,
            data_regiao_nordeste, data_regiao_norte)


def corrige_coordenadas(df):
    # Ao analisar os datasets foi notado que existem muitas coordenadas
    # duplicadas o que gera dados geográficos errados. Essa função
    # corrige essas coordenadas buscando as corretas através do endereço
    # usando a Geocoding API do Google Maps
    print('Entrando no loop de correção de coordenadas')
    for index, row in df.iterrows():
        logradouro = row['no_logradouro']
        numero = row['nu_endereco']
        bairro = row['no_bairro']
        uf = row['uf']
        endereco = (str(logradouro) + ', ' + str(numero) +
                    ', ' + str(bairro) + ', ' + str(uf))
        print(endereco)
        novas_coordenadas_dict = get_coordenadas(endereco)
        lat = novas_coordenadas_dict['lat']
        long = novas_coordenadas_dict['long']
        endereco_gmaps = novas_coordenadas_dict['endereco']
        df.loc[index, 'lat_corrigida'] = lat
        df.loc[index, 'long_corrigida'] = long
        df.loc[index, 'endereco_google'] = endereco_gmaps
    return df


def grava_arquivo(dataset, file_name):
    file_path = 'D:\\repos\\study\\mestrado\\artigos\\UBS\\instancias\\'
    dataset.to_csv(file_path+file_name, sep=';', index=False, header=True)


def le_instancia_grafo(file_name):
    file = 'D:\\repos\\study\\mestrado\\artigos\\UBS\\instancias\\%s' \
        % file_name
    print(file)
    df_distancias = pd.DataFrame()
    f = open(file, 'r')
    count_lines = 0
    for line in f:
        count_lines += 1
        if count_lines == 1:
            qtd_nos = int(line.split('\t')[0])
            qtd_arestas = int(line.split('\t')[1])
        else:
            if count_lines > (qtd_nos + 1):
                origem = line.split('\t')[0]
                destino = line.split('\t')[1]
                distancia = line.split('\t')[2]
                distancia = float(distancia.split('\n')[0])
                new_register = pd.DataFrame({'origem': origem,
                                             'destino': destino,
                                             'distancia': distancia},
                                            index=[0])
                df_distancias = df_distancias.append(new_register,
                                                     ignore_index=True)
    df_distancias.reset_index(inplace=True)
    return df_distancias
