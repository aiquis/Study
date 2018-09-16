import numpy as np
from learningCurve import learningCurve
import matplotlib.pyplot as plt
import scipy.io as spio


mat = spio.loadmat('ex5data1.mat', squeeze_me=True)

X = mat['X']
y = mat['y']

Xtest = mat['Xtest']
ytest = mat['ytest']

Xval = mat['Xval']
yval = mat['yval']

X_ones = np.c_[np.ones(X.shape[0]), X]
Xval_ones = np.c_[np.ones(Xval.shape[0]), Xval]

erro_treino, erro_validacao = learningCurve(X_ones, y, Xval_ones, yval, 0)

plt.plot(np.arange(1, 13), erro_treino,
         label='Train', color='purple')
plt.plot(np.arange(1, 13), erro_validacao,
         label='Cross Validation', color='green')
plt.title('Learning curve for linear regression')
plt.xlabel('Number of training examples')
plt.ylabel('Error')
plt.legend()
plt.show()
