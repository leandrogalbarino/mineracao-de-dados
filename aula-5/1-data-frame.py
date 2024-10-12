import pandas as pd
import numpy as np

X = [    ['A', 'B', 'C', 'E', 'F'],
    ['A', 'B', 'C', 'E', 'F'],
    ['G', 'A', 'D', 'H', 'B'],
    ['G', 'A', 'D', 'H', 'B'],
    ['I', 'J', 'A', 'D', 'F']
]

dfY = pd.DataFrame()
df = pd.DataFrame(X, columns=['Col1', 'Col2', 'Col3', 'Col4', 'Col5'])

array_np = np.zeros(10)
array_list = [1,2,3,4,5,1,3,4]

# Obter tamanho linhas e colunas do Data Frame
print(f"Linhas DataFrame:{df.shape[0]}")
print(f"Colunas DataFrame:{df.shape[1]}")

#Tamanho do Array com Numpy e Lista
print(f"Tamanho do array nump: {array_np.size}")
print(f"Tamanho do array nump: {len(array_list)}")
input()
