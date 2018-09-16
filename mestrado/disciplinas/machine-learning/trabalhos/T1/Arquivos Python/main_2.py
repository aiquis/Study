import pandas as pd
from normalizacao import normalizar_caracteristicas

dataset = pd.read_csv('ex1data2.txt', header=None)

x = dataset.iloc[:, 0:-1].values
y = dataset.iloc[:, -1:].values

(x_norm,
 y_norm,
 mean_x,
 std_x,
 mean_y,
 std_y,
 norm_values_dict) = normalizar_caracteristicas(x, y)
print("x_norm: " + "\n" + str(x_norm) + "\n",
      "y_norm: " + "\n" + str(y_norm) + "\n",
      "mean_x: " + str(mean_x) + "\n",
      "std_x: " + str(std_x) + "\n",
      "mean_y: " + str(mean_y) + "\n",
      "std_y: " + str(std_y))
