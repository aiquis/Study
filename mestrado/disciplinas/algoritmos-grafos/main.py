import pandas as pd
import numpy as np
from graph_funcs import calcula_distancia, cria_grafo, dijkstra, prim


def main():
    # Caminho e nome dos arquivos de dados
    file_path = r'C:\\Users\\aiqui\\Dropbox\\CEFET\\Disciplinas' \
        r'\\Algoritmos em Grafos\\Trabalho\Dados\\'
    file_name = 'ubs_funcionamentonone.csv'

    data = pd.read_csv(file_path + file_name, sep=',')
    # Criando um dataset só de dados do RJ
    data_rj = data[data['uf'] == 'RJ']  # 1880 rows
    data_rj = data_rj.reset_index()
    # Criando versão reduzida do dataset pra testes
    data_rj_reduzido = data_rj[0:5]
    # Cria um grafo com estrutura de dicionário à partir de um
    # Pandas DataFrame. Dicionários são o padrão do Python
    # para representação de grafos
    # Referência: https://www.python.org/doc/essays/graphs/
    grafo = cria_grafo(data_rj_reduzido)
    print('Grafo: \n', grafo)
    # Prompt para o usuário selecionar qual problema gostaria de resolver
    # Problema 1 - Menor distância entre duas UBS (com opçaõ de remoção)
    # O problema 1 é um problema de caminhos mínimos
    # Problema 2 - Menos distância para se percorrer todas as UBS
    # O problema 2 é um problema de Árvore Geradora Mínima
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
            if input3 != input_ubs1 and input3 != input_ubs2:
                data_rj_reduzido = data_rj_reduzido[data_rj_reduzido['gid'] !=
                                                    int(input3)]
                data_rj_reduzido = data_rj_reduzido.reset_index()
                grafo = cria_grafo(data_rj_reduzido)
                print('Novo caminho mínimo entre as unidades: \n')
                caminho_minimo, distancia_minima = dijkstra(grafo,
                                                            int(input_ubs1),
                                                            int(input_ubs2),
                                                            [], {}, {})
                print('Novo caminho mínimo = ', caminho_minimo,
                      ' com distância de: ', distancia_minima, 'Km')
            else:
                print('Não é possível remover esse nó pois é '
                      'o ponto de partidaou destino da sua busca')
        else:
            print('Finalizando programa')
    elif int(input1) == 2:
        prim(grafo)
    else:
        print('Opção não encontrada. Finalizando o programa')


if __name__ == "__main__":
    main()
