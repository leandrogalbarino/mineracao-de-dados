import pandas as pd
import numpy as np
X = [    ['A', 'B', 'C', 'E', 'F'],
    ['A', 'B', 'C', 'E', 'F'],
    ['G', 'A', 'D', 'H', 'B'],
    ['G', 'A', 'D', 'H', 'B'],
    ['I', 'J', 'A', 'D', 'F']
]

df = pd.DataFrame(X, columns=['Col1', 'Col2', 'Col3', 'Col4', 'Col5'])

valores_unicos = np.unique(df.values)
print(f"Data Frame:\n {df}")

print(f"Valores únicos ordenados: {np.sort(valores_unicos)}")

item_verificacao = 'K'
if item_verificacao in valores_unicos:
    print(f"O item '{item_verificacao}' está presente nos dados.")
else:
    print(f"O item '{item_verificacao}' não está presente nos dados.")

# Para pausar o programa antes de sair
input()