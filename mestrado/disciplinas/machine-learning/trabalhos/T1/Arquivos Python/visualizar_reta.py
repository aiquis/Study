dataset = pd.read_csv('ex1data1.txt', header = None)

X = dataset.iloc[:, 0:-1].values
y = dataset.iloc[:, -1:].values

t = np.arange(0, 25, 1)
plt.scatter(X, y, color='red', marker='x', label='Training Data')
plt.plot(t, theta[0] + (theta[1]*t), colors='blue', label='Linear Regression')
plt.axis([4, 25, -5, 25])
plt.title('População da cidade x Lucro da filial')
plt.xlabel('População da cidade (10k)')
plt.ylabel('Lucro (10k)')
plt.legend()
plt.show()
