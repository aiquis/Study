import numpy as np
import random as rn
import h5py
from neural_net import (preprocessing_neural, create_model_neural,
                        train_model_neural)
from conv_net import preprocessing_cnn, create_model_cnn, train_model_cnn
import matplotlib.pyplot as plt
import os
import tensorflow as tf
from keras import backend as K


# Comando necessário para que o código tenha reproducibilidade
# para certas operações hash-based
os.environ['PYTHONHASHSEED'] = '0'

np.random.seed(42)
rn.seed(12345)

session_conf = tf.ConfigProto(intra_op_parallelism_threads=1,
                              inter_op_parallelism_threads=1)

tf.set_random_seed(1234)

sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
K.set_session(sess)


def load_dataset():
    train_dataset = h5py.File('train_catvnoncat.h5', 'r')
    # Your train set features
    train_set_x_orig = np.array(train_dataset["train_set_x"][:])
    # Your train set labels
    train_set_y_orig = np.array(train_dataset["train_set_y"][:])

    test_dataset = h5py.File('test_catvnoncat.h5', 'r')
    # Your test set features
    test_set_x_orig = np.array(test_dataset["test_set_x"][:])
    # Your test set labels
    test_set_y_orig = np.array(test_dataset["test_set_y"][:])

    # The list of classes
    classes = np.array(test_dataset["list_classes"][:])

    train_set_y_orig = train_set_y_orig.reshape(-1, train_set_y_orig.shape[0])
    test_set_y_orig = test_set_y_orig.reshape(-1, test_set_y_orig.shape[0])

    return (train_set_x_orig, train_set_y_orig, test_set_x_orig,
            test_set_y_orig, classes)


def evaluate_model(model, x, y):
    score = model.evaluate(x, y)
    print('Loss value: {}'.format(score[0]))
    print('Accuracy: {}'.format(score[1]))


def plot_accuracy(history):
    # Loss Curves
    plt.figure(figsize=[8, 6])
    plt.plot(history.history['loss'], 'r', linewidth=3.0)
    plt.plot(history.history['val_loss'], 'b', linewidth=3.0)
    plt.legend(['Training loss', 'Validation Loss'], fontsize=18)
    plt.xlabel('Epochs ', fontsize=16)
    plt.ylabel('Loss', fontsize=16)
    plt.title('Loss Curves', fontsize=16)
    plt.show()

    # Accuracy Curves
    plt.figure(figsize=[8, 6])
    plt.plot(history.history['acc'], 'r', linewidth=3.0)
    plt.plot(history.history['val_acc'], 'b', linewidth=3.0)
    plt.legend(['Training Accuracy', 'Validation Accuracy'], fontsize=18)
    plt.xlabel('Epochs ', fontsize=16)
    plt.ylabel('Accuracy', fontsize=16)
    plt.title('Accuracy Curves', fontsize=16)
    plt.show()


def main():

    ################################################
    # Parte 1: REDE NEURAL FULLY CONNECTED
    ################################################

    # Carregando os datasets de treinamento e teste
    train_set_x, train_set_y, test_set_x, test_set_y, classes = load_dataset()
    train_set_y = train_set_y.reshape(-1, 1)
    test_set_y = test_set_y.reshape(-1, 1)

    # Aplicando pré-processamento nos vetores de features
    train_set_x, train_set_y = preprocessing_neural(train_set_x, train_set_y)
    test_set_x, test_set_y = preprocessing_neural(test_set_x, test_set_y)
    print(train_set_x.shape)
    print(train_set_y.shape)
    input_shape = train_set_x.shape[1:]
    print(input_shape)

    # Criando o modelo de rede neural para predição
    batch_size = 15
    epochs = 100
    model = create_model_neural(input_shape)
    hist_neural = train_model_neural(model, train_set_x, train_set_y,
                                     test_set_x, test_set_y,
                                     batch_size, epochs)
    evaluate_model(model, test_set_x, test_set_y)
    plot_accuracy(hist_neural)

    ################################################
    # Parte 2: REDE CONVOLUCIONAL
    ################################################

    train_set_x, train_set_y, test_set_x, test_set_y, classes = load_dataset()
    train_set_y = train_set_y.reshape(-1, 1)
    test_set_y = test_set_y.reshape(-1, 1)

    # Aplicando pré-processamento nos vetores de features
    train_set_x, train_set_y = preprocessing_cnn(train_set_x, train_set_y)
    test_set_x, test_set_y = preprocessing_cnn(test_set_x, test_set_y)
    print(train_set_x.shape)
    print(train_set_y.shape)
    input_shape = train_set_x[0].shape
    print(input_shape)

    # Criando o modelo de rede neural para predição
    batch_size = 10
    epochs = 60
    model = create_model_cnn(input_shape)
    hist_cnn = train_model_cnn(model, train_set_x, train_set_y,
                               test_set_x, test_set_y,
                               batch_size, epochs)
    evaluate_model(model, test_set_x, test_set_y)
    plot_accuracy(hist_cnn)


if __name__ == "__main__":
    main()
