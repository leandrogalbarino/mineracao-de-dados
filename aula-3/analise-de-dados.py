import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x = np.random.randint(1, 60, 40)
media = np.mean(x)
mediana = np.median(x)
quartis = np.percentile(x, [25, 50, 75])
desvio_padrao = np.std(x)

plt.plot(x, 'bo', label='Valores')
plt.ylim(0, 60)
plt.ylabel('Valores')

plt.text(2, 55, f'Media: {np.median(x):.2f}', fontsize=12)
plt.text(2, 50, f'Mediana: {mediana:.2f}', fontsize=12)
plt.text(2, 45, f'1º Quartil: {quartis[0]:.2f}', fontsize=12)
plt.text(2, 40, f'3º Quartil: {quartis[2]:.2f}', fontsize=12)
plt.text(2, 35, f'Desvio Padrão: {desvio_padrao:.2f}', fontsize=12)

plt.show()
input("Digite enter para fechar")
