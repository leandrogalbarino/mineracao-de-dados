import json
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import re


def mostrar_df_one_hot(df, tipo):
    print(f"\nDataFrame Final com Doce {tipo} One-Hot Encoding:")
    print(f"{df}\n")

def mostrar_grafico_ocorrencias(item_counts, tipo):
    plt.figure(figsize=(12, 10))
    plt.bar(item_counts.index, item_counts.values, color='skyblue')
    plt.xlabel('Itens')
    plt.ylabel('Frequência')
    plt.title(f'Frequência de Itens com Doce {tipo}')
    plt.xticks(rotation=20, ha='right')
    plt.show()

def formatar_produtos(produtos, tipo):
    produtos_formatados = []  # Lista para armazenar os produtos formatados
    for produto in produtos:
        produto = re.sub(r'[^\w\s-]', '', produto)
        produto = produto.strip().capitalize()

        if 'doce' in produto.lower():
            if tipo == 'generico':
                produto = "Doce"
            else:
                produto = re.sub(r'^\b(Do\w*)', 'Doce', produto, flags=re.IGNORECASE)
        produto = re.sub(r'^\b(Ca\w*)', 'Café', produto, flags=re.IGNORECASE)
        produto = re.sub(r'^\b(Pã\w*)', 'Pão', produto, flags=re.IGNORECASE)
        produto = re.sub(r'^\b(Pr\w*)', 'Presunto', produto, flags=re.IGNORECASE)
        produto = re.sub(r'^\b(Qu\w*)', 'Queijo', produto, flags=re.IGNORECASE)
        produto = re.sub(r'^\b(Pa\w*)', 'Pastel', produto, flags=re.IGNORECASE)
        produto = re.sub(r'^\b(Re\w*)', 'Refri', produto, flags=re.IGNORECASE)

        produtos_formatados.append(produto)

    return produtos_formatados

def graficos_regras_de_associacao(regras):
    regras = regras.copy()
    # Converte os produtos de frozenset para string para visualização
    regras.loc[:, 'antecedents_str'] = regras['antecedents'].apply(lambda x: ', '.join(list(x)))
    regras.loc[:, 'consequents_str'] = regras['consequents'].apply(lambda x: ', '.join(list(x)))


    fig, axes = plt.subplots(1, 3, figsize=(18, 6))  

    # Gráfico de Suporte
    axes[0].bar(regras['antecedents_str'] + ' => ' + regras['consequents_str'], regras['support'], color='lightgreen')
    axes[0].set_title('Suporte', fontsize=15)
    axes[0].set_ylabel('Suporte', fontsize=12)
    axes[0].set_ylim(0, max(regras['support']) + 0.05)

    # Gráfico de Confiança
    axes[1].bar(regras['antecedents_str'] + ' => ' + regras['consequents_str'], regras['confidence'], color='skyblue')
    axes[1].set_title('Confiança', fontsize=15)
    axes[1].set_ylabel('Confiança', fontsize=12)
    axes[1].set_ylim(0, 1) 

    # Gráfico de Lift
    axes[2].bar(regras['antecedents_str'] + ' => ' + regras['consequents_str'], regras['lift'], color='salmon')
    axes[2].set_title('Lift', fontsize=15)
    axes[2].set_ylabel('Lift', fontsize=12)
    axes[2].set_ylim(0, max(regras['lift']) + 1)

    # Definindo os ticks e os rótulos
    for ax in axes:
        ax.set_xticks(range(len(regras)))  
        ax.set_xticklabels(regras['antecedents_str'] + ' => ' + regras['consequents_str'], rotation=90, ha='right')

    plt.tight_layout()  # Ajusta o layout para não cortar os rótulos
    plt.show()


# Caminho do arquivo Json
caminho_arquivo = 'C:\\Users\\leand\\OneDrive\\Documentos\\meus-projetos\\algoritmos-python\\mineracao-dados\\Trabalho1\\padaria_trab.json'

# Abrindo e lendo o arquivo JSON
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

# Converte o JSON para DataFrame e remove a coluna 'compra'
df = pd.json_normalize(dados)
if 'compra' in df.columns:
    df = df.drop(columns=['compra'])

# Formata a coluna "produtos" para realizar a mineração
if 'produtos' in df.columns:
    # Aplica a função formatar_produtos linha por linha
    df['produtos'] = df['produtos'].apply(lambda x: formatar_produtos(x, "normal"))
    df['produtos2'] = df['produtos'].apply(lambda x: formatar_produtos(x, "generico"))


# Mineração de Dados
# 1. Explodindo a coluna de produtos
df_explodir = df.explode('produtos')
df_explodir_doce = df.explode('produtos2')

# 2. Aplicando o one-hot encoding
df_one_hot = pd.get_dummies(df_explodir['produtos'])
df_one_hot_doce = pd.get_dummies(df_explodir_doce['produtos2'])

# 3. Agrupando e somando as ocorrências
df_final = df_one_hot.groupby(df_explodir.index).sum()
df_final2 = df_one_hot_doce.groupby(df_explodir_doce.index).sum()

# 4. Convertendo os valores para True ou False
df_final = df_final.astype(bool)
df_final2 = df_final2.astype(bool)

# 4-1. Etapa para analisar se os dados estão corretos
# Exibindo o Data Frame com One-Hot Encoding
mostrar_df_one_hot(df_final, "com Marca")
mostrar_df_one_hot(df_final2, "Genérico")

# 5. Aplicando o Principio Apriori:
conjuntos_frequentes = apriori(df_final, min_support=0.06, use_colnames=True)
conjuntos_frequentes2 = apriori(df_final2, min_support=0.06, use_colnames=True)

# 6. Gerando regras de associação
regras = association_rules(conjuntos_frequentes, metric="lift", min_threshold=0.6)
regras2 = association_rules(conjuntos_frequentes2, metric="lift", min_threshold=0.6)

# 7. Mostrando Frequencia dos itens através de um gráfico
contagem_itens = df_final.sum().sort_values(ascending=False)
contagem_itens2 = df_final2.sum().sort_values(ascending=False)
mostrar_grafico_ocorrencias(contagem_itens, "com Marca")
mostrar_grafico_ocorrencias(contagem_itens2, "Genérico")

# 8. Exibindo todas as regras de associação encontradas
print("\nRegras de Associação:")
print(f"\nTotal de regras de associação encontradas: {len(regras)}")
print(regras[['antecedents', 'consequents', 'support',
      'confidence', 'lift']].to_string(index=False))

# 9. Exibir as 5 principais regras de associação
top_regras = regras.sort_values('lift', ascending=False).head(5)
print("\nAs 5 principais regras de associação:")
print(top_regras[['antecedents', 'consequents', 'support',
      'confidence', 'lift']].to_string(index=False))

# 10. Exibir a regra mais influente
regra_maior_lift = regras.loc[regras['lift'].idxmax()]
print("\nA regra mais influente (produto 1 para 1):")
print(f"{list(regra_maior_lift['antecedents'])} => {
      list(regra_maior_lift['consequents'])}")

# 11. Exibir as regras que implicam Doce
regras_com_doce = regras2[regras2['consequents'].apply(lambda x: 'Doce' in x)]
print("\nRegras que implicam a compra de 'Doce':")
print(regras_com_doce[['antecedents', 'consequents',
      'support', 'confidence', 'lift']].to_string(index=False))

#12. Mostra um gráfico com as regras de associação
graficos_regras_de_associacao(regras)
graficos_regras_de_associacao(regras_com_doce)

input()  # Esperar tecla
