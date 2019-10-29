import requests
import geopy.distance
import googlemaps


GOOGLE_API_KEY = 'Inserir aqui API Key do Google Maps '
BING_API_KEY = 'Inserir aqui API Key do Bing Maps'


def get_coordenadas(endereco):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': endereco, 'key': GOOGLE_API_KEY}
    print('Fazendo request para receber novas coordenadas')
    r = requests.get(url=url, params=params)
    res = r.json()
    coordenadas = {}
    if (r.status_code == 200 and res['status'] != 'OVER_QUERY_LIMIT'):
        print('Request com sucesso')
        if res['status'] == 'OK':
            print('RESPONSE GEOCODE', res)
            result = res['results'][0]
            coordenadas = {'lat': result['geometry']['location']['lat'],
                           'long': result['geometry']['location']['lng'],
                           'endereco': result['formatted_address']}
        elif res['status'] == 'ZERO_RESULTS':
            print('Endereço não encontrado')
            coordenadas = {'lat': 0,
                           'long': 0,
                           'endereco': 'Não encontrado'}
    else:
        print('Erro no request ou limite por dia atingido')
        coordenadas = {'lat': -1,
                       'long': -1,
                       'endereco': 'Não encontrado'}
    print(coordenadas)
    return(coordenadas)


def calcula_distancia_gmaps(cidade_1, cidade_2):
    # Função recebe dois nós e calcula a distância em metros
    # entre eles à partir das coordenadas
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    origem = (str(cidade_1['lat_corrigida']) + ',' +
              str(cidade_1['long_corrigida']))
    print(origem)
    destino = (str(cidade_2['lat_corrigida']) + ',' +
               str(cidade_2['long_corrigida']))
    print(destino)
    params = {'origins': origem, 'destinations': destino,
              'key': GOOGLE_API_KEY, 'mode': 'driving'}
    r = requests.get(url=url, params=params)
    if r.status_code == 200:
        res = r.json()
        print('RESPONSE DISTANCE MAXTRIX', res)
        if res['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
            # Quando não houver um caminho de carro entre os pontos
            # distancia = 1000000 para não ser entendido como um
            # caminho rápido entre dois pontos (o que poderia
            # acontecer se colocasse distancia = 0)
            distancia = 1000000
        else:
            distancia = res['rows'][0]['elements'][0]['distance']['value']
        print('Coord1: ' + str(origem))
        print('Coord2: ' + str(destino))
        print('Distância: ' + str(distancia))
    else:
        print('Erro no request')
    return distancia


def calcula_distancia_bing(cidade_1, cidade_2):
    # Função recebe dois nós e calcula a distância em km
    # entre eles à partir das coordenadas
    url = 'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix'
    origem = (str(cidade_1['lat_corrigida']) + ',' +
              str(cidade_1['long_corrigida']))
    print(origem)
    destino = (str(cidade_2['lat_corrigida']) + ',' +
               str(cidade_2['long_corrigida']))
    print(destino)
    params = {'origins': origem, 'destinations': destino,
              'key': BING_API_KEY, 'travelMode': 'driving'}
    r = requests.get(url=url, params=params, timeout=600)
    if r.status_code == 200:
        res = r.json()
        print('RESPONSE DISTANCE MAXTRIX', res)
        distancia = res['resourceSets'][0]['resources'][0]['results'][0]['travelDistance']
        print('Coord1: ' + str(origem))
        print('Coord2: ' + str(destino))
        print('Distância: ' + str(distancia))
    else:
        print('Erro no request')
    return distancia


def calcula_distancia(cidade_1, cidade_2):
    # Função recebe dois nós e calcula a distância em Km
    # entre eles à partir das coordenadas
    coord1 = (cidade_1['lat'], cidade_1['long'])
    coord2 = (cidade_2['lat'], cidade_2['long'])
    return int(geopy.distance.distance(coord1, coord2).km)
