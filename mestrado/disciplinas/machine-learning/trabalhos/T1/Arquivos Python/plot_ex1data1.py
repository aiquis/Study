import matplotlib.pyplot as plt

filepath = "\ex1data1.txt"

def importarDados(filepath,names):
    path = os.getcwd() + filepath  
    data = pd.read_csv(path, header=None, names=names)

    # adiciona uma coluna de 1s referente a variavel x0
    data.insert(0, 'Ones', 1)
    
    # separa os conjuntos de dados x (caracteristicas) e y (alvo)
    cols = data.shape[1]  
    X = data.iloc[:,0:cols-1]  
    y = data.iloc[:,cols-1:cols]
    
    # converte os valores em numpy arrays
    X = np.array(X.values)  
    y = np.array(y.values)
    
    return X,y

X,y = importarDados(filepath,["Population","Profit"])

plt.scatter(X, y, color='red', marker='x')
plt.title('População da cidade x Lucro da filial')
plt.xlabel('População da cidade (10k)')
plt.ylabel('Lucro (10k)')
plt.savefig('plot1.1.png')
plt.show()
