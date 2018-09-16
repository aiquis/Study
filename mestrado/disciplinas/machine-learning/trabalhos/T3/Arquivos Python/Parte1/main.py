from cofi_cost_func import cofi_cost_func
from load_movie_list import load_movie_list
from normalize_ratings import normalize_ratings
from matplotlib import use, cm
use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from scipy.optimize import minimize

# ===== Carga do arquivo de avaliações de filmes ======

print('Loading movie ratings dataset.')

#  Load data
data = scipy.io.loadmat('../data/ex8_movies.mat')
Y = data['Y']
R = data['R'].astype(bool)
# Y é uma matriz de ordem 1682x943, que contém avaliações (1-5)
# de 1682 filmes sobre 943 usuários
# R é uma matriz 1682x943, em que R(i,j) = 1 se
# e somente se o usuário j avaliou ofilme i

# A partir da matriz, é possível computar estatísticas como a avaliação média.
print('Avaliação média para filme 1 (Toy Story): %f / 5' % np.mean(Y[0, R[0, :]]))

# É também possível ter uma perspectiva gráfica das avaliações com o comando imagesc

plt.figure()
plt.imshow(Y, aspect='equal', origin='upper', extent=(0, Y.shape[1], 0, Y.shape[0]/2.0))
plt.ylabel('Movies')
plt.xlabel('Users')
plt.show()

#================================================================================
## ============ Função de Custo da Filtragem Colaborativa ===========
#  Para essa seção, você deve implementar o código da função de custo da
#  filtragem colaborativa. Para ajudá-lo a depurar o código da sua função, 
#  são fornecidos um conjunto de parâmetros pré-treinados. Especificamente,  
#  você deve completar o código em cofi_cost_func.py para retornar o valor de J.

# Carrega os parâmetros previamente treinados (X, Theta, num_users, num_movies, num_features)
data = scipy.io.loadmat('../data/ex8_movieParams.mat')
X = data['X']
Theta = data['Theta']
num_users = data['num_users']
num_movies = data['num_movies']
num_features = data['num_features']

#  Reduz o conjunto de dados para que a execução seja mais rápida
num_users = 4
num_movies = 5
num_features = 3
X = X[:num_movies, :num_features]
Theta = Theta[:num_users, :num_features]
Y = Y[:num_movies, :num_users]
R = R[:num_movies, :num_users]

#  Avaliação da função de custo
J, grad = cofi_cost_func(np.hstack((X.T.flatten(), Theta.T.flatten())), Y, R, num_users, num_movies,
               num_features, 0)
           
print('Custo computado usando parâmetros pré-treinados: %f \n(valor deve ser próximo de 22.22)' % J)


#================================================================================
## ============== Definição de avaliações para um novo usuário ===============
#  Antes de treinar o modelo de filtragem colaborativa, essa seção primeiro adiciona
#  algumas avaliações que correspondem a um novo usuário. Essa parte do código
#  irá também permitir que você defina suas próprias avaliações para filmes
#  no conjunto de dados.
#
movieList = load_movie_list()

#  Inicia o vetor de avaliações do novo usuário
my_ratings = np.zeros(1682)

# Verifique o arquivo movie_idx.txt para encontrar o id de cada filme
# Por exemplo, Toy Story (1995) tem ID 1; sendo assim, para atribuir avaliação "4", faça:
my_ratings[0] = 4

# Ou suponha que você não gostou de Silence of the Lambs (1991):
my_ratings[97] = 2

# Abaixo, são definidas as avaliações para outros filmes:
my_ratings[6] = 3
my_ratings[11] = 5
my_ratings[53] = 4
my_ratings[63] = 5
my_ratings[65] = 3
my_ratings[68] = 5
my_ratings[182] = 4
my_ratings[225] = 5
my_ratings[354] = 5

print('Avaliações do novo usuário:')
for i in range(len(my_ratings)):
    if my_ratings[i] > 0:
        print('\tAvaliou %d para %s' % (my_ratings[i], movieList[i]))

## ================== Aprendizado de Recomendações para Filmes ====================
#  Essa seção realiza o treinamento do modelo de filtragem colaborativa usando como 
#  entrada o conjunto de dados de avaliações de filmes de 1682 filmes e 943 usuários
#

print('\nTreinamento da filtragem colaborativa...')

#  Carga dos dados
data = scipy.io.loadmat('../data/ex8_movies.mat')
Y = data['Y']
R = data['R'].astype(bool)

#  Adiciona algumas avaliações à matriz
Y = np.column_stack((my_ratings, Y))
R = np.column_stack((my_ratings, R)).astype(bool)

#  Normaliza avaliações
Ynorm, Ymean = normalize_ratings(Y, R)

num_users = Y.shape[1]
num_movies = Y.shape[0]
num_features = 10

# Define parâmetros iniciais (Theta, X)
X = np.random.rand(num_movies, num_features)
Theta = np.random.rand(num_users, num_features)

initial_parameters = np.hstack((X.T.flatten(), Theta.T.flatten()))

# fator de regularização
Lambda = 10

costFunc = lambda p: cofi_cost_func(p, Ynorm, R, num_users,num_movies, num_features, Lambda)[0]
gradFunc = lambda p: cofi_cost_func(p, Ynorm, R, num_users, num_movies, num_features, Lambda)[1]

result = minimize(costFunc, initial_parameters, method='CG', jac=gradFunc,
                  options={'disp': True, 'maxiter': 1000.0})
theta = result.x
cost = result.fun


# Extrai as matrizes X e Theta a partir de theta
X = theta[:num_movies * num_features].reshape(num_movies, num_features)
Theta = theta[num_movies * num_features:].reshape(num_users, num_features)

print('Aprendizado do Sistema de Recomendação finalizado.')

## ================== Realização de recomendações ====================
#  Após treinamento do modelo, é possível realizar recomendações por meio
#  da computação da matriz de predições.
#

p = X.dot(Theta.T)
my_predictions = p[:, 0] + Ymean

movieList = load_movie_list()

# ordena predições em ordem decrescente
pre=np.array([[idx, p] for idx, p in enumerate(my_predictions)])
post = pre[pre[:,1].argsort()[::-1]]
r = post[:,1]
ix = post[:,0]

print('\nRecomendações principais:')
for i in range(10):
    j = int(ix[i])
    print('\tPrevisão de avaliação %.1f para %s' % (my_predictions[j], movieList[j]))

print('\nAvaliações originais fornecidas:')
for i in range(len(my_ratings)):
    if my_ratings[i] > 0:
        print('\tAvaliou %d para %s' % (my_ratings[i], movieList[i]))