import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix


def feature_normalization(x):
    min_max_scaler = preprocessing.MinMaxScaler()
    return min_max_scaler.fit_transform(x)


def train_neural_network(x, y):
    # Mudando o formato do array para 1d array pois é o formato que o
    # classificador pede
    y = np.ravel(y)
    clf = MLPClassifier(hidden_layer_sizes=(1, 5), solver='lbfgs',
                        alpha=0.00001, activation='relu',
                        max_iter=1000, random_state=42)
    trained_model = clf.fit(x, y)
    return trained_model


def create_confusion_matrix(y_true, y_pred):
    return confusion_matrix(y_true, y_pred)


def main():
    # Carregando o conjunto de dados de treinamento
    dataset = pd.read_csv('credtrain.txt', names=['ESCT', 'NDEP', 'RENDA',
                          'TIPOR', 'VBEM', 'NPARC', 'VPARC', 'TEL', 'IDADE',
                          'RESMS', 'ENTRADA', 'CLASSE'], sep='\t')
    # Criando o vetor X de features com as features do conjunto de dados
    X_train = np.array(dataset[['ESCT', 'NDEP', 'RENDA',
                                'TIPOR', 'VBEM', 'NPARC', 'VPARC', 'TEL',
                                'IDADE', 'RESMS', 'ENTRADA']])
    # Criando o vetor de classificação y do conjunto de dados de treinamento
    y_train = np.array(dataset['CLASSE']).reshape(-1, 1)
    # Checando se os formatos estão de acordo com os pedidos no enunciado
    print(X_train.shape)
    print(y_train.shape)
    # Normalizando o vetor de features pra que todos os valores
    # fiquem entre 0 e 1 (Min-Max Normalization)
    X_train = feature_normalization(X_train)

    # Carregando o conjunto de dados de teste
    dataset = pd.read_csv('credtest.txt', names=['ESCT', 'NDEP', 'RENDA',
                          'TIPOR', 'VBEM', 'NPARC', 'VPARC', 'TEL', 'IDADE',
                          'RESMS', 'ENTRADA', 'CLASSE'], sep='\t')
    # Criando o vetor X de features com as features do conjunto de teste
    X_test = np.array(dataset[['ESCT', 'NDEP', 'RENDA',
                               'TIPOR', 'VBEM', 'NPARC', 'VPARC', 'TEL',
                               'IDADE', 'RESMS', 'ENTRADA']])
    # Criando o vetor de classificação y do conjunto de dados de teste
    y_test = np.array(dataset['CLASSE']).reshape(-1, 1)
    # Normalizando o vetor de features pra que todos os valores
    # fiquem entre 0 e 1 (Min-Max Normalization)
    X_test = feature_normalization(X_test)

    model = train_neural_network(X_train, y_train)

    # Testando o modelo treinado
    y_pred = model.predict(X_test)
    scores = cross_val_score(model, X_test, np.ravel(y_test), cv=10)
    print("Precisão: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    conf_matrix = create_confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = conf_matrix.ravel()
    print('Confusion Matrix:' '\n'
          'True negatives: ' + str(tn) + '\n'
          'False positives: ' + str(fp) + '\n'
          'False negatives: ' + str(fn) + '\n'
          'True positives: ' + str(tp) + '\n')


if __name__ == "__main__":
    main()
