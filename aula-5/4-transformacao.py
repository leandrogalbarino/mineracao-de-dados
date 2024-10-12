import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Definindo semente
np.random.seed(42)

x = pd.DataFrame({
    "var1": np.random.choice(range(1, 6), size=10),
    "var2": np.random.choice(range(6, 11), size=10),
    "var3": np.random.choice(range(11, 16), size=10)
}
)

# Somando 1 no index
# x.index = x.index + 1

# Renomeando as linhas usando rename
# Melhor, pois pode renomear apenas as linhas que desejar
# x = x.rename(index={0: 'Linha1', 1: 'Linha2', 2: 'Linha3', 3: 'Linha4',
#              4: 'Linha5', 5: 'Linha6', 6: 'Linha7', 7: 'Linha8', 8: 'Linha9'})

# Renomeando usando index
# x = x.index = ['Linha1', 'Linha2', 'Linha3', 'Linha4', 'Linha5', 'Linha6', 'Linha7', 'Linha8', 'Linha9', 'Linha10']

for i in range(2, 6):
    if x.loc[i, 'var2'] > 5 and x.loc[i, 'var2'] < 10:
        print(x.loc[i, 'var2'])
    if np.x.loc[i].nan:
        print(x.loc[i])
print(x)
