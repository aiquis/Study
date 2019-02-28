import pandas as pd
import numpy as np


def cria_instancias(data):
    # Criação de dataset pra UBSs do estado do RJ
    data_estado_rj = data[data['uf'] == 'RJ']
    data_estado_rj.reset_index(inplace=True)

    # Criação de dataset pra UBSs do estado do SP
    data_estado_sp = data[data['uf'] == 'SP']
    data_estado_sp.reset_index(inplace=True)

    # Criação de dataset para UBSs do estado de MG
    data_estado_mg = data[data['uf'] == 'MG']
    data_estado_mg.reset_index(inplace=True)

    # Criação de dataset pra cidade do RJ
    data_cidade_rio = data[(data['uf'] == 'RJ') &
                           (data['cidade'] == 'Rio de Janeiro')]
    data_cidade_rio.reset_index(inplace=True)

    # Criação de dataset pra cidade de SP
    data_cidade_saopaulo = data[(data['uf'] == 'SP') &
                                (data['cidade'] == 'São Paulo')]
    data_cidade_saopaulo.reset_index(inplace=True)

    # Criação de dataset pra região sudeste
    data_regiao_sudeste = data[(data['uf'] == 'RJ') | (data['uf'] == 'SP') |
                               (data['uf'] == 'MG') | (data['uf'] == 'ES')]
    data_regiao_sudeste.reset_index(inplace=True)

    # Criação de dataset para região sul
    data_regiao_sul = data[(data['uf'] == 'PR') | (data['uf'] == 'SC') |
                           (data['uf'] == 'RS')]
    data_regiao_sul.reset_index(inplace=True)

    # Criação de dataset para região nordeste
    data_regiao_nordeste = data[(data['uf'] == 'BA') | (data['uf'] == 'SE') |
                                (data['uf'] == 'AL') | (data['uf'] == 'PE') |
                                (data['uf'] == 'PE') | (data['uf'] == 'PB') |
                                (data['uf'] == 'RN') | (data['uf'] == 'CE') |
                                (data['uf'] == 'PI') | (data['uf'] == 'MA')]
    data_regiao_nordeste.reset_index(inplace=True)

    # Criação de dataset para região norte
    data_regiao_norte = data[(data['uf'] == 'TO') | (data['uf'] == 'PA') |
                             (data['uf'] == 'AP') | (data['uf'] == 'RR') |
                             (data['uf'] == 'AM') | (data['uf'] == 'RO') |
                             (data['uf'] == 'AC')]

    return (data_estado_rj, data_estado_sp, data_estado_mg, data_cidade_rio,
            data_cidade_saopaulo, data_regiao_sudeste, data_regiao_sul,
            data_regiao_nordeste, data_regiao_norte)


def main():
    # Caminho e nome dos arquivos de dados
    file_path = r'C:\\Users\\aiqui\\Dropbox\\CEFET\\Disciplinas' \
        r'\\Algoritmos em Grafos\\Trabalho\Dados\\'
    file_name = 'ubs_funcionamentonone.csv'

    # Leitura do arquivo de dados
    data = pd.read_csv(file_path + file_name, sep=',')
    print(data.info())


if __name__ == "__main__":
    main()
