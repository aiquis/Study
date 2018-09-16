import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.io import loadmat
from scipy import stats


def estimate_gaussian_params(X):
    # Vetor mu recebe a média de cada feature de X
    mu = np.mean(X, axis=0)
    # Vetor sigma2 recebe a variância de cada feature de X
    sigma2 = np.var(X, axis=0)
    return (mu, sigma2)


def select_epsilon(pval, yval):
    best_epsilon_value = 0
    best_f1_value = 0

    step_size = (pval.max() - pval.min()) / 1000

    print('step size: ' + str(step_size))

    for epsilon in np.arange(pval.min(), pval.max(), step_size):
        preds = pval < epsilon
        # Calculando verdadeiros positivos.
        # Rótulo diz que é uma anômalia e foi
        # corretamente previsto como uma
        true_positive = np.sum(np.logical_and(preds == 1, yval == 1))
        # Calculando falsos positivos.
        # Rótulo diz que não é uma anômalia, mas foi
        # previsto como uma
        false_positive = np.sum(np.logical_and(preds == 1, yval == 0))
        # Calculando falsos negativos.
        # Rótulo diz que é uma anômalia, mas não foi
        # previsto como uma
        false_negative = np.sum(np.logical_and(preds == 0, yval == 1))

        # Calculando a precisão do nosso algoritmo dado um
        # determinado valor de epsilon
        prec = true_positive / (true_positive + false_positive)
        rec = true_positive / (true_positive + false_negative)
        f1 = (2 * prec * rec) / (prec + rec)

        # Selecionando o melhor valor de epsilon, ou seja,
        # o com maior precisão
        if f1 > best_f1_value:
            best_f1_value = f1
            best_epsilon_value = epsilon
    return best_epsilon_value, best_f1_value


def main():
    data = loadmat('../data/ex8data1.mat')
    X = data['X']

    (mu, sigma2) = estimate_gaussian_params(X)
    print('mu: ' + str(mu))
    print('variance: ' + str(sigma2))

    # Plot dataset
    plt.scatter(X[:, 0], X[:, 1], marker='x')
    plt.axis('equal')
    plt.show()

    # Plot dataset and contour lines
    plt.scatter(X[:, 0], X[:, 1], marker='x')
    x = np.arange(0, 25, .025)
    y = np.arange(0, 25, .025)
    first_axis, second_axis = np.meshgrid(x, y)
    Z = mlab.bivariate_normal(first_axis, second_axis,
                              np.sqrt(sigma2[0]), np.sqrt(sigma2[1]),
                              mu[0], mu[1])
    plt.contour(first_axis, second_axis, Z, 10, cmap=plt.cm.jet)
    plt.axis('equal')
    plt.show()

    # Load validation dataset
    Xval = data['Xval']
    yval = data['yval'].flatten()

    stddev = np.sqrt(sigma2)

    pval = np.zeros((Xval.shape[0], Xval.shape[1]))
    pval[:, 0] = stats.norm.pdf(Xval[:, 0], mu[0], stddev[0])
    pval[:, 1] = stats.norm.pdf(Xval[:, 1], mu[1], stddev[1])
    print(np.prod(pval, axis=1).shape)
    epsilon, _ = select_epsilon(np.prod(pval, axis=1), yval)
    print('Best value found for epsilon: ' + str(epsilon))

    # Computando a densidade de probabilidade
    # de cada um dos valores do dataset em
    # relação a distribuição gaussiana
    p = np.zeros((X.shape[0], X.shape[1]))
    p[:, 0] = stats.norm.pdf(X[:, 0], mu[0], stddev[0])
    p[:, 1] = stats.norm.pdf(X[:, 1], mu[1], stddev[1])

    # Apply model to detect abnormal examples in X
    anomalies = np.where(np.prod(p, axis=1) < epsilon)

    # Plot the dataset X again, this time highlighting the abnormal examples.
    plt.clf()
    plt.scatter(X[:, 0], X[:, 1], marker='x')
    plt.scatter(X[anomalies[0], 0], X[anomalies[0], 1], s=50,
                color='r', marker='x')
    plt.axis('equal')
    plt.show()


if __name__ == "__main__":
    main()
