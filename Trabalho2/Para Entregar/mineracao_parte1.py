import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Função para carregar e concatenar arquivos .xls
def carregar_dados(caminho_arquivos):
    arquivos = glob.glob(f"{caminho_arquivos}/*.xls")
    print(f"Arquivos encontrados: {arquivos}")
    
    lista_dataframes = []
    for arquivo in arquivos:
        df = pd.read_excel(arquivo)
        nome_arquivo = os.path.basename(arquivo).split()[0]
        df['nome_predio'] = nome_arquivo
        lista_dataframes.append(df)
    
    return pd.concat(lista_dataframes, ignore_index=True)

# Carregar e limpar dados
df = carregar_dados("./dados").dropna().drop(columns=['NIVEL_CURSO'])
df['Taxa_Conclusao'] = (df['FORMADOS'] / df['INGRESSANTES']).replace([np.inf, -np.inf], 0).fillna(0)

# Visualização: Relação entre Ingressantes e Formados
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x='INGRESSANTES', y='FORMADOS', hue='Taxa_Conclusao', palette='viridis')
plt.title('Relação entre Formados e Taxa de Ingressantes')
plt.xlabel('Ingressantes')
plt.ylabel('Formados')
plt.legend(title='Taxa de Conclusão')
plt.show()

# Agrupamento por curso
df_agrupado = df.groupby('NOME_UNIDADE').agg(
    ingressantes_total=('INGRESSANTES', 'sum'),
    formados_total=('FORMADOS', 'sum')
).reset_index()

df_agrupado['Taxa_Conclusao_Curso'] = (df_agrupado['formados_total'] / df_agrupado['ingressantes_total']).replace([np.inf, -np.inf], 0).fillna(0)
df_agrupado['taxa_evasao'] = 1 - df_agrupado['Taxa_Conclusao_Curso']

# Carregar e limpar dados
df = carregar_dados("./dados").dropna().drop(columns=['NIVEL_CURSO'])

# Agrupar por unidade, somando ingressantes e formados ao longo dos anos e pegando o primeiro prédio
df_agrupado_total = df.groupby('NOME_UNIDADE').agg(
    ingressantes_total=('INGRESSANTES', 'sum'),
    formados_total=('FORMADOS', 'sum'),
    nome_predio=('nome_predio', 'first')  # Ou 'unique', se desejar todos
).reset_index()

# Calcular taxa de conclusão e taxa de evasão
df_agrupado_total['Taxa_Conclusao_Curso'] = (df_agrupado_total['formados_total'] / df_agrupado_total['ingressantes_total']).replace([np.inf, -np.inf], 0).fillna(0)
df_agrupado_total['taxa_evasao'] = 1 - df_agrupado_total['Taxa_Conclusao_Curso']

df_filtrado = df_agrupado_total[(df_agrupado_total['formados_total'] > 0) & (df_agrupado_total['ingressantes_total'] > 0)]


# Cursos com maior taxa de evasão (Top 10)
top_10_evasao = df_filtrado.nlargest(10, 'taxa_evasao')[['NOME_UNIDADE', 'taxa_evasao', 'nome_predio']]

print("Top 10 cursos com maior taxa de evasão:")
print(top_10_evasao)

# Visualizar cursos com maior taxa de evasão
plt.figure(figsize=(12, 6))
sns.barplot(data=top_10_evasao, x='NOME_UNIDADE', y='taxa_evasao', hue='nome_predio', palette='magma')
plt.title('Top 10 Cursos com Maior Taxa de Evasão')
plt.xlabel('Nome da Unidade')
plt.ylabel('Taxa de Evasão')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np

# Selecionar as colunas de interesse
X = df_filtrado[['Taxa_Conclusao_Curso', 'taxa_evasao']]

# Normalizar os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# Aplicar K-Means com o número ótimo de clusters (por exemplo, 3)
kmeans = KMeans(n_clusters=3, random_state=42)
df_filtrado['Cluster'] = kmeans.fit_predict(X_scaled)


# Visualização: Relação entre Taxa de Conclusão e Taxa de Evasão por Prédio (Aproximado)
plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=df_filtrado,
    x='Taxa_Conclusao_Curso',
    y='taxa_evasao',
    hue='nome_predio',
    palette='tab20',
    style='nome_predio',
    s=100
)

plt.title('Relação entre Taxa de Conclusão e Taxa de Evasão por Prédio (Zoom)')
plt.xlabel('Taxa de Conclusão')
plt.ylabel('Taxa de Evasão')

# Limitar os eixos a 0-3
plt.xlim(0, 1)
plt.ylim(0, 1)

plt.legend(title='Prédio', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

df['ANO'] = pd.to_datetime(df['ANO'], format='%Y', errors='coerce')

df_timeline = df.groupby('ANO').agg(
    ingressantes=('INGRESSANTES', 'sum'),
    formados=('FORMADOS', 'sum')
).reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_timeline, x='ANO', y='ingressantes', label='Ingressantes', marker='o')
sns.lineplot(data=df_timeline, x='ANO', y='formados', label='Formados', marker='o')

plt.title('Evolução de Ingressantes e Formados ao Longo dos Anos')
plt.xlabel('Ano')
plt.ylabel('Número de Estudantes')
plt.grid(True)
plt.legend()
plt.show()


# Filtrar os dados entre 0 e 1
df_filtrado_restrito = df_filtrado[
    (df_filtrado['Taxa_Conclusao_Curso'] >= 0) & 
    (df_filtrado['Taxa_Conclusao_Curso'] <= 1) & 
    (df_filtrado['taxa_evasao'] >= 0) & 
    (df_filtrado['taxa_evasao'] <= 1)
]

# Selecionar as colunas para clustering
X_restrito = df_filtrado_restrito[['Taxa_Conclusao_Curso', 'taxa_evasao']]

# Normalizar os dados
scaler = StandardScaler()
X_scaled_restrito = scaler.fit_transform(X_restrito)

# Aplicar K-Means com 3 clusters
kmeans_restrito = KMeans(n_clusters=3, random_state=42)
df_filtrado_restrito['Cluster'] = kmeans_restrito.fit_predict(X_scaled_restrito)

# Visualizar clusters
plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=df_filtrado_restrito, 
    x='Taxa_Conclusao_Curso', 
    y='taxa_evasao', 
    hue='Cluster', 
    palette='viridis', 
    style='nome_predio', 
    s=100
)
plt.title('Clusters de Taxa de Conclusão e Evasão (Ajustado entre 0 e 1)')
plt.xlabel('Taxa de Conclusão')
plt.ylabel('Taxa de Evasão')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.grid(True)
plt.tight_layout()
plt.show()


# Contagem de cursos por prédio e cluster
contagem_clusters = df_filtrado_restrito.groupby(['nome_predio', 'Cluster']).size().reset_index(name='Quantidade')

# Calcular o total de cursos por prédio
total_por_predio = contagem_clusters.groupby('nome_predio')['Quantidade'].transform('sum')

# Adicionar coluna de porcentagem
contagem_clusters['Porcentagem'] = (contagem_clusters['Quantidade'] / total_por_predio) * 100

# Exibir o resultado
print(contagem_clusters)
