import numpy as np
import matplotlib.pyplot as plt

dias = np.array([1,2,3,4,5,6,7])
vendas = np.array([50, 60, 55, 70, 65, 80, 90])

plt.plot(dias, vendas, marker='v', color="blue", label='Vendas')


plt.figure(num='Vendasss')
plt.title('Vendas ao Longo dos Dias')
plt.xlabel('Dias')
plt.ylabel('Quantidade de Vendas')

plt.legend()
plt.grid(True)

plt.show()