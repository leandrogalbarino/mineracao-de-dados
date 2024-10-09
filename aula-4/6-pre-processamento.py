import pandas as pd
import numpy as np

#Data frame
data = {'valores': [1, 2, np.nan, 5, 6, np.nan]}
df = pd.DataFrame(data)

#Media sem NA
media = df['valores'].mean()
print(f"Média (ignorando NA): {media}")

#Dados faltantes, retorna se as colunas que tem dados faltantes
faltante = df.isnull().any()
print("\nDados faltando em cada coluna:")
print(faltante)

#Calcula quantos na tem no Data frame
print("Quanto sao na")
print(df.isna().sum())

#Cria um Data Frame removendo os na
df_sem_nan = df.dropna()
print(df_sem_nan)
print("\nDataFrame após remover linhas com NaN:")
print(df_sem_nan)

#Preenche o Data frame base com a media, onde tem na
df = df['valores'].fillna(media)
print("\nDataFrame após substituir NaN pela média:")
print(df)



