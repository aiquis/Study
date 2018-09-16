from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.utils import to_categorical


def preprocessing_cnn(x, y):
    # Função para aplicar pré-processamento nos vetores
    # de features e target

    # Normalizando os valores de RGB
    x_flatten = x.astype('float32')
    x_flatten = x_flatten/255

    y_cat = to_categorical(y)

    return x_flatten, y_cat


def create_model_cnn(input_shape):
    model = Sequential()
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu',
              input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    return model


def train_model_cnn(model, x_train, y_train, x_test, y_test, batch, epoch):
    model.compile(optimizer='sgd', loss='categorical_crossentropy',
                  metrics=['accuracy'])
    print(model.summary())
    history = model.fit(x_train, y_train, batch_size=batch, epochs=epoch,
                        validation_data=(x_test, y_test), shuffle=False)
    return history
