import pandas as pd
import numpy as np
# Transforme Z de modo que cada item diferente seja um atributo (coluna própria). Então para cada linha o
# atributo recebe “SIM” caso enteja presente e “NÃO”
# caso esteja ausente
url = 'https://www-usr.inf.ufsm.br/~joaquim/UFSM/DM/ds/z.csv'

df = pd.read_csv(url, header=None)
valores_unicos = np.sort(np.unique(df.values))

df_transformado = pd.DataFrame()
for valor in valores_unicos:
    df_transformado[str(valor)] = df.apply(lambda row: 'SIM' if valor in row.values else 'NÃO', axis=1) 

print(df)
print(df_transformado.head())
