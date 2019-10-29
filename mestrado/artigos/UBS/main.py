import pandas as pd
import numpy as np
from graph_funcs import (cria_grafo_networkx,
                         desenha_grafo,
                         cria_instancia_grafo,
                         roda_shortest_path_mst,
                         roda_funcoes_centralidade,
                         calculo_centro_grafo,
                         elimina_arestas,
                         caminhos_minimos_um_no)
from instancias import (cria_instancias, corrige_coordenadas,
                        grava_arquivo, le_instancia_grafo)


def main():
    # Passa nome do arquivo txt com infos do grafo a ser carregado
    grafo_file_name = 'grafo_cidade_saopaulo_consolidado_2.txt'
    prefix_file_name = 'cidade_saopaulo'
    # Função lê o arquivo e retorna um DataFrame Pandas
    grafo_df = le_instancia_grafo(grafo_file_name)
    print(grafo_df.info())

    # Chamando função de criação de grafo usando NetworkX
    # É retornado um objeto grafo NetworkX
    grafo_networkx = cria_grafo_networkx(grafo_df)
    # Chama a função que executa funções pré-determinadas
    # para o grafo NetworkX
    # Em caso de necessidade de eliminar arestas, descomentar a linha abaixo
    # grafo_cidade_incompleto = elimina_arestas(grafo_networkx, 20)
    roda_shortest_path_mst(grafo_networkx, prefix_file_name)
    roda_funcoes_centralidade(grafo_networkx, prefix_file_name)
    calculo_centro_grafo(grafo_networkx)
    # Em caso de necessidade de executar caminho mínimo a partir
    # de um nó, descomentar a linha abaixo
    # caminhos_minimos_um_no(grafo_rj_incompleto, '39740', prefix_file_name)


if __name__ == "__main__":
    main()
