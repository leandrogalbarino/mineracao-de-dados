import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o CSV diretamente da web
url = 'https://www-usr.inf.ufsm.br/~joaquim/UFSM/DM/ds/LD00c.csv'
df = pd.read_csv(url)


# Exibindo estatísticas descritivas
print("\nEstatísticas descritivas:")
print(df.describe())

plt.figure(figsize=(10,6))
sns.boxplot(data=df[['Precipitacao']])
plt.title('Boxplot das Variáveis Numéricas')


input()