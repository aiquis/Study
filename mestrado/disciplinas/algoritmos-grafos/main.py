import pandas as pd
import numpy as np
import sys
from graph_funcs import calcula_distancia, cria_grafo, dijkstra


def main():
    file_path = r'C:\\Users\\aiqui\\Dropbox\\CEFET\\Disciplinas' \
        r'\\Algoritmos em Grafos\\Trabalho\Dados\\'
    file_name = 'ubs_funcionamentonone.csv'

    data = pd.read_csv(file_path + file_name, sep=',')
    # Criando um dataset só de dados do RJ
    data_rj = data[data['uf'] == 'RJ']  # 1880 rows
    data_rj = data_rj.reset_index()
    # Criando versão reduzida do dataset pra testes
    data_rj_reduzido = data_rj[0:5]
    grafo = cria_grafo(data_rj_reduzido)
    input1 = input('Digite o código do seu problema: \n'
                   '1 - Menor distância entre UBS \n'
                   '2 - Melhor caminho para entrega de remédios \n')
    if int(input1) == 1:
        print('Essas são as UBS em funcionamento: \n')
        print('Código - Nome - Cidade \n')
        for index, row in data_rj_reduzido.iterrows():
            codigo = row['gid']
            nome = row['no_fantasia']
            cidade = row['cidade']
            print(str(codigo) + ' - ' + nome + ' - ' + cidade + '\n')
        print('Quer saber a menor distância entre quais unidades? \n')
        input_ubs1 = input('Unidade 1 (código): \n')
        input_ubs2 = input('Unidade 2 (código): \n')
        # teste bom: (179, 152) = 75 distancia
        caminho_minimo, distancia_minima = dijkstra(grafo, int(input_ubs1),
                                                    int(input_ubs2))
        print('Caminho mínimo = ', caminho_minimo, ' com distância de: ',
              distancia_minima, 'Km')

        input3 = input('Deseja simular o fechamento de algum UBS? \n'
                       'Digite o código da unidade ou tecle '
                       '"Enter" para sair \n')
        if input3:
            data_rj_reduzido = data_rj_reduzido[data_rj_reduzido['gid'] !=
                                                int(input3)]
            data_rj_reduzido = data_rj_reduzido.reset_index()
            grafo = cria_grafo(data_rj_reduzido)
            print('Novo caminho mínimo entre as unidades: \n')
            caminho_minimo, distancia_minima = dijkstra(grafo, int(input_ubs1),
                                                        int(input_ubs2),
                                                        [], {}, {})
            print('Caminho mínimo = ', caminho_minimo, ' com distância de: ',
                  distancia_minima, 'Km')
        else:
            print('Finalizando programa')
    else:
        print('Ainda não implementado')


if __name__ == "__main__":
    main()
