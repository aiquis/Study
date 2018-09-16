import pandas as pd
import matplotlib.pyplot as plt


dataset = pd.read_csv("ex2data2.txt", header=None,
                      names=['teste1', 'teste2', 'resultado'])


aprovado = dataset[dataset['resultado'].isin([1])]
rejeitado = dataset[dataset['resultado'].isin([0])]

fig, ax = plt.subplots(figsize=(12, 8))

ax.scatter(aprovado['teste1'], aprovado['teste2'],
           s=50, c='k', marker='+', label='y = 1')

ax.scatter(rejeitado['teste1'], rejeitado['teste2'],
           s=50, c='y', marker='o', label='y = 0')
ax.legend()
ax.set_xlabel('Microchip Test 1')
ax.set_ylabel('Microchip Test 2')
plt.show()
