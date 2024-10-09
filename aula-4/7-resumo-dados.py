import pandas as pd

data = {'valores': [1, 2, 3, 4, 5]}
df = pd.DataFrame(data)

resumo = df['valores'].describe()
maximo = resumo['max']
minimo = resumo['min']

print(resumo)
print(f"maximo: {maximo}")
print(f"minimo: {minimo}")