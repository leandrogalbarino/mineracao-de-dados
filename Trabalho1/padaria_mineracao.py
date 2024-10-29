import json
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import re

def formatar_produto(produto):
    produto = produto.strip().capitalize()  # Remove espaços em branco extras e capitaliza
    # Substituições específicas de prefixo
    produto = re.sub(r'^\b(Ca\w*)', 'Café', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Pã\w*)', 'Pão', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Pr\w*)', 'Presunto', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Qu\w*)', 'Queijo', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Pa\w*)', 'Pastel', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Do\w*)', 'Doce', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Re\w*)', 'Refri', produto, flags=re.IGNORECASE)
    return produto

def formatar_produtos(produtos):
    return [formatar_produto(produto) for produto in produtos]

#CAMINHO ARTHUR
# caminho_arquivo = 'C:\\Users\\arthu\\OneDrive\Documentos\\ThuRar\\CienciaDaComputacao_UFSM\\2024.2\Mineração de Dados\\T1_Leandro\\mineracao-de-dados\\Trabalho1\\padaria_trab.json'
# caminho_novo_arquivo = 'C:\\Users\\arthu\\OneDrive\Documentos\\ThuRar\\CienciaDaComputacao_UFSM\\2024.2\Mineração de Dados\\T1_Leandro\\mineracao-de-dados\\Trabalho1\\produtos_atualizados.json'

#CAMINHO LEANDRO
caminho_arquivo = 'C:\\Users\\leand\\OneDrive\\Documentos\\meus-projetos\\algoritmos-python\\mineracao-dados\\Trabalho1\\padaria_trab.json'
caminho_novo_arquivo = 'C:\\Users\\leand\\OneDrive\\Documentos\\meus-projetos\\algoritmos-python\\mineracao-dados\\Trabalho1\\produtos_atualizados.json'

# Abrindo e lendo o arquivo JSON
with open(caminho_arquivo, 'r') as arquivo:
    dados = json.load(arquivo)

# Converte o JSON para DataFrame e remove a coluna 'compra' (se necessário)
df = pd.json_normalize(dados)
if 'compra' in df.columns:
    df = df.drop(columns=['compra'])

# Formata a coluna "produtos" para realizar a mineração
if 'produtos' in df.columns:
    df['produtos'] = df['produtos'].apply(formatar_produtos)

# Criando e escrevendo o DataFrame no novo arquivo JSON
df.to_json(caminho_novo_arquivo, orient='records', lines=True, force_ascii=False)

# 1. Explodindo a coluna de produtos
df_exploded = df.explode('produtos')

# 2. Aplicando o one-hot encoding
df_one_hot = pd.get_dummies(df_exploded['produtos'])

# 3. Agrupando e somando as ocorrências
df_final = df_one_hot.groupby(df_exploded.index).sum()

# 4. Convertendo os valores para True ou False
df_final = df_final.astype(bool)

# Exibindo o resultado final
print("DataFrame Final com One-Hot Encoding:")
print(df_final)


# Principio Apriori:
frequent_itemsets = apriori(df_final, min_support=0.06, use_colnames=True)

# Gerando regras de associação
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.6)


item_counts = df_final.sum().sort_values(ascending=False)
print("\nFrequência de itens:")
print(item_counts)


# Exibindo as regras encontradas
print("\nRegras de Associação:")
print(f"\nTotal de regras de associação encontradas: {len(rules)}")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_string(index=False))

# 1. Exibir as 5 principais regras
top_rules = rules.sort_values('lift', ascending=False).head(5)
print("\nAs 5 principais regras de associação:")
print(top_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_string(index=False))

# 2. Encontrar a regra mais influente
max_lift_rule = rules.loc[rules['lift'].idxmax()]

print("\nA regra mais influente (produto 1 para 1):")
print(f"{list(max_lift_rule['antecedents'])} => {list(max_lift_rule['consequents'])}")
input() # esperar tecla

