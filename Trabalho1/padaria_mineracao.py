import json
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import re


def mostrar_grafico_ocorrencias(item_counts):
    plt.figure(figsize=(12, 10))
    plt.bar(item_counts.index, item_counts.values, color='skyblue')
    plt.xlabel('Itens')
    plt.ylabel('Frequência')
    plt.title('Frequência de Itens')
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

# CAMINHO ARTHUR
# caminho_arquivo = 'C:\\Users\\arthu\\OneDrive\Documentos\\ThuRar\\CienciaDaComputacao_UFSM\\2024.2\Mineração de Dados\\T1_Leandro\\mineracao-de-dados\\Trabalho1\\padaria_trab.json'
# caminho_novo_arquivo = 'C:\\Users\\arthu\\OneDrive\Documentos\\ThuRar\\CienciaDaComputacao_UFSM\\2024.2\Mineração de Dados\\T1_Leandro\\mineracao-de-dados\\Trabalho1\\produtos_atualizados.json'


# CAMINHO LEANDRO
caminho_arquivo = 'C:\\Users\\leand\\OneDrive\\Documentos\\meus-projetos\\algoritmos-python\\mineracao-dados\\Trabalho1\\padaria_trab.json'
caminho_novo_arquivo = 'C:\\Users\\leand\\OneDrive\\Documentos\\meus-projetos\\algoritmos-python\\mineracao-dados\\Trabalho1\\produtos_atualizados.json'

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
df_exploded = df.explode('produtos')
df_exploded_doce = df.explode('produtos2')

# 2. Aplicando o one-hot encoding
df_one_hot = pd.get_dummies(df_exploded['produtos'])
df_one_hot_doce = pd.get_dummies(df_exploded_doce['produtos2'])

# 3. Agrupando e somando as ocorrências
df_final = df_one_hot.groupby(df_exploded.index).sum()
df_final2 = df_one_hot_doce.groupby(df_exploded_doce.index).sum()

# 4. Convertendo os valores para True ou False
df_final = df_final.astype(bool)
df_final2 = df_final2.astype(bool)

# 4-1. Etapa para analisar se os dados estão corretos
# Exibindo o Data Frame com One-Hot Encoding
print("DataFrame Final com One-Hot Encoding:")
print(df_final)

# 5. Aplicando o Principio Apriori:
frequent_itemsets = apriori(df_final, min_support=0.06, use_colnames=True)
frequent_itemsets2 = apriori(df_final2, min_support=0.06, use_colnames=True)

# 6. Gerando regras de associação
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.6)
rules2 = association_rules(frequent_itemsets2, metric="lift", min_threshold=0.6)

# 7. Mostrando Frequencia dos itens através de um gráfico
item_counts = df_final.sum().sort_values(ascending=False)
item_counts2 = df_final2.sum().sort_values(ascending=False)

mostrar_grafico_ocorrencias(item_counts)
mostrar_grafico_ocorrencias(item_counts2)

# 8. Exibindo todas as regras de associação encontradas
print("\nRegras de Associação:")
print(f"\nTotal de regras de associação encontradas: {len(rules)}")
print(rules[['antecedents', 'consequents', 'support',
      'confidence', 'lift']].to_string(index=False))

# 9. Exibir as 5 principais regras de associação
top_rules = rules.sort_values('lift', ascending=False).head(5)
print("\nAs 5 principais regras de associação:")
print(top_rules[['antecedents', 'consequents', 'support',
      'confidence', 'lift']].to_string(index=False))

# 10. Exibir a regra mais influente
max_lift_rule = rules.loc[rules['lift'].idxmax()]
print("\nA regra mais influente (produto 1 para 1):")
print(f"{list(max_lift_rule['antecedents'])} => {
      list(max_lift_rule['consequents'])}")


# 11. Exibir as regras que implicam Doce
rules_with_doce = rules2[rules2['consequents'].apply(lambda x: 'Doce' in x)]
print("\nRegras que implicam a compra de 'Doce':")
print(rules_with_doce[['antecedents', 'consequents',
      'support', 'confidence', 'lift']].to_string(index=False))

input()  # esperar tecla
