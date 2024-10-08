import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#1 Crie um vetor de caracteres com a sequência 1 ate 99. Chame de vet1.
vet1 = [i for i in range(1,100)]
print(vet1)

#2 - Crie uma matrix 4x4 com valores de 1 até 16. Chame de mat1.
mat = [[(i * 4 + j + 1) for j in range(4)] for i in range(4)]
print(mat)

#3 - Crie um data frame com a matriz anterior. Chame de DF1.
#4 - Coloque nomes nas colunas do data frame (‘a’,‘b’,‘c’,‘d’).
df = pd.DataFrame(mat, columns=['coluna A', 'Coluna B', 'Coluna C', 'Coluna D'], index=['A','B','C','D'])
print(df)

#5 - Crie uma lista com a,b,c. Depois substitua o ‘b’ por 2. Chame de lista1.
lista1 = ['a']
lista1.extend(['b','c'])
a = lista1.index('b')
lista1[a] = 2
print(lista1)

#6 - Verifique que, em lista1, 2 é um valor numérico.
print(type(lista1.index(2)))

#7 - Use a função summary para prever dados de sua matriz.
print(df.describe(include='all'))

#8 - Use um laço para criar um vetor chamado vet2 com a fórmula: vet1[i](i0.8), onde i é o índice do laço (1 … 99).
vet2 = []
for i in range(1,100):
    vet2.append(vet1[i - 1]*(i**0.8))
print()
print(vet2)

#9 - Use plot e hist para visualizar o vetor vet2.
plt.figure(figsize=(12,6))

plt.subplot(1, 2, 1)
plt.plot(vet2, marker='o', linestyle = '-', color='b')
plt.title('Grafico do vet2')
plt.xlabel('índice')
plt.ylabel('Valores de v2')
plt.grid()

plt.subplot(1,2,2)
plt.hist(vet2, bins=10, color='c', edgecolor='black')
plt.title('Histograma de vet2')
plt.xlabel('Valores de vet2')
plt.ylabel(' Frequencia')
plt.grid()

plt.tight_layout()
plt.show()

#10 - Verifique a média, mediana e o terceiro quartil do vetor vet2.
media = np.mean(vet2)
mediana = np.median(vet2)
terceiro_quartil = np.percentile(vet2, 75)

print(f"Média de vet2: {media:.2f}")
print(f"Mediana de vet2: {mediana:.2f}")
print(f"Terceiro Quartil de vet2: {terceiro_quartil:.2f}")

#11 - Carregue um arquivo .csv usando as funções url e read.csv.
url = 'https://www-usr.inf.ufsm.br/~joaquim/UFSM/DM/ds/Insetos00.csv'
df = pd.read_csv(url, encoding='latin1')
print(df.head())