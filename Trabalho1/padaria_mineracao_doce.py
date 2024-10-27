import json
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import re

def formatar_produto(produto, string_a, string_final):
    # Remove especificações e mantém apenas o nome
    produto = re.sub(r'\s[^,]*$', '', produto)
    if produto.lower().startswith(string_a):
        return string_final

    return produto.capitalize()

def formatar_produtos(produtos):
    return [
        formatar_produto(produto.strip(), 'ca', 'Café') if 'ca' in produto.lower() else
        formatar_produto(produto.strip(), 'pã', 'Pão') if 'pã' in produto.lower() else
        formatar_produto(produto.strip(), 'pr', 'Presunto') if 'pr' in produto.lower() else
        formatar_produto(produto.strip(), 'qu', 'Queijo') if 'qu' in produto.lower() else
        formatar_produto(produto.strip(), 'pa', 'Pastel') if 'pa' in produto.lower() else
        formatar_produto(produto.strip(), 'do', 'Doce') if 'ca' in produto.lower() else
        formatar_produto(produto.strip(), 're', 'Refri') if 'ca' in produto.lower() else
        re.sub(r'\s[^,]*$', '', produto.strip()) for produto in produtos
    ]

#caminho_arquivo = 'C:\\Users\\leand\\OneDrive\\Documentos\\meus-projetos\\algoritmos-python\\mineracao-dados\\Trabalho1\\padaria_trab.json'
#caminho_novo_arquivo = 'C:\\Users\\leand\\OneDrive\\Documentos\\meus-projetos\\algoritmos-python\\mineracao-dados\\Trabalho1\\produtos_atualizados.json'
caminho_arquivo = 'C:\\Users\\arthu\\OneDrive\Documentos\\ThuRar\\CienciaDaComputacao_UFSM\\2024.2\Mineração de Dados\\T1_Leandro\\mineracao-de-dados\\Trabalho1\\padaria_trab.json'
caminho_novo_arquivo = 'C:\\Users\\arthu\\OneDrive\Documentos\\ThuRar\\CienciaDaComputacao_UFSM\\2024.2\Mineração de Dados\\T1_Leandro\\mineracao-de-dados\\Trabalho1\\produtos_atualizados.json'

# Abrindo e lendo o arquivo JSON
with open(caminho_arquivo, 'r') as arquivo:
    dados = json.load(arquivo)

# Agora, 'dados' contém o conteúdo do arquivo JSON como um dicionário
df = pd.json_normalize(dados)

# Remove a coluna "compra" irrelevante para a Mineração
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


# Principio Apriori:
frequent_itemsets = apriori(df_final, min_support=0.1, use_colnames=True)

# Gerando regras de associação
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# 3. Regras que implicam a compra de "Doce"
rules_with_doce = rules[rules['consequents'].apply(lambda x: 'Doce' in x)]
print("\nRegras que implicam a compra de 'Doce':")
print(rules_with_doce[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_string(index=False))

input()