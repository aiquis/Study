import pandas as pd
import numpy as np
from graph_funcs import (cria_grafo_networkx,
                         desenha_grafo,
                         cria_instancia_grafo,
                         roda_funcoes_artigo)
from instancias import (cria_instancias, corrige_coordenadas,
                        grava_arquivo, le_instancia_grafo)


def main():
    # Passa nome do arquivo txt com infos do grafo a ser carregado
    grafo_file_name = 'grafo_cidade_rio.txt'
    # Função lê o arquivo e retorna um DataFrame Pandas
    grafo_df = le_instancia_grafo(grafo_file_name)
    print(grafo_df.info())

    # Chamando função de criação de grafo usando NetworkX
    # É retornado um objeto grafo NetworkX
    grafo_networkx = cria_grafo_networkx(grafo_df)
    # Chama a função que executa funções pré-determinadas
    # para o grafo NetworkX
    roda_funcoes_artigo(grafo_networkx)


if __name__ == "__main__":
    main()
