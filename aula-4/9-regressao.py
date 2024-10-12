import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


xa = np.array([3, 5, 6, 7, 9, 14, 16, 16, np.nan, 27, 34, 50, 61])
ya = np.zeros(xa.size - 1)

for i in range(xa.size - 1):
    ya[i] = xa[i + 1]

xa = xa[:-1].reshape(-1, 1)

model = LinearRegression()
model.fit(xa, ya)

# Coeficiente e intercepto
print(f"Coeficiente: {model.coef_}")
print(f"Intercepto: {model.intercept_}")

last_value = np.array([[61]])  # Último valor de xa


xa_flat = xa.flatten()
df = pd.DataFrame({'x': xa_flat, 'y': ya})

# Criando um gráfico de dispersão com uma linha de ajuste
sns.lmplot(x='x', y='y', data=df)

plt.show()
