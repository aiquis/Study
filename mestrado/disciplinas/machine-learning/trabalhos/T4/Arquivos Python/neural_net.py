import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.utils import to_categorical


def preprocessing_neural(x, y):
    # Função para aplicar pré-processamento nos vetores
    # de features e target

    # Achatando o número de dimensões do vetor de features
    # Isso significa que estamos transformando nossa
    # matriz de imagens de 64x64 num vetor no formato (nSamples, 64x64)
    # que será servido para a rede neural como uma única feature
    x_flatten = x.reshape(x.shape[0], -1)

    # Normalizando os valores de RGB para ficarem entre 0 e 1
    x_flatten = x_flatten.astype('float32')
    x_flatten = x_flatten/255

    # Transformando os valores inteiros de y em categorias
    # por ser o formato necessário para o Keras realizar a
    # classificação de múltiplas classes
    y_cat = to_categorical(y)

    return x_flatten, y_cat


def create_model_neural(input_shape):
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=input_shape))
    model.add(Dense(2, activation='softmax'))
    return model


def train_model_neural(model, x_train, y_train, x_test, y_test, batch, epoch):
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy',
                  metrics=['accuracy'])
    print(model.summary())
    history = model.fit(x_train, y_train, batch_size=batch, epochs=epoch,
                        validation_data=(x_test, y_test), shuffle=False)
    return history
