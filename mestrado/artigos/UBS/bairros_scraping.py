import pandas as pd
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode


def get_bairros_por_distrito(artigos_dict):
    # Essa função faz um scraping em páginas da Folha de São Paulo
    # que contém as listas de bairros por distritos e gera um CSV
    # com os resultados
    for k, v in artigos_dict.items():
        req = requests.get(v)
        if req.status_code == 200:
            print('Requisição com sucesso')
            content = req.content
        else:
            print('Erro na requisição', req.status_code)
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find(name = 'table')
        # Pelo formato das tabelas é necessário iterar no html da tabela
        # para conseguir obter uma nova tabela com bairros e distritos
        # como colunas. Nesse momento será adota uma soluçao mais suja
        # que vai demandar um ajuste manual
        # TO DO: fazer todo o tratamento e criação do DF em código
        df = pd.read_html(str(table))[0]
        df = df[df.columns[0]].str.upper()
        df = df.apply(unidecode)
        df.to_csv('D:\\repos\\study\\mestrado\\artigos\\UBS\\resultados\\bairros_' + str(k) + '_sp.csv', header=['distrito'])


def main():
    artigos_dict = {'norte': 'https://www1.folha.uol.com.br/cotidiano/2012/10/1164607-confira-todos-os-distritos-e-bairros-da-zona-norte-de-sp.shtml',
                    'sul': 'https://www1.folha.uol.com.br/cotidiano/2012/10/1163859-confira-todos-os-distritos-e-bairros-da-zona-sul-de-sp.shtml',
                    'oeste': 'https://www1.folha.uol.com.br/cotidiano/2012/10/1164789-confira-todos-os-distritos-e-bairros-da-zona-oeste-de-sp.shtml',
                    'leste': 'https://www1.folha.uol.com.br/cotidiano/2012/10/1164604-veja-todos-os-distritos-e-bairros-da-zona-leste-de-sp.shtml',
                    'centro': 'https://www1.folha.uol.com.br/cotidiano/2012/10/1164880-conheca-todos-os-distritos-e-bairros-da-regiao-central-de-sp.shtml'
                    }
    get_bairros_por_distrito(artigos_dict)


if __name__ == "__main__":
    main()
