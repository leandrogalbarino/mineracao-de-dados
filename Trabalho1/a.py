import re
import pandas as pd

def formatar_produto(produto):
    # Remove caracteres indesejados
    produto = re.sub(r'[^\w\s-]', '', produto)
    produto = produto.strip().capitalize()  # Remove espaços em branco extras e capitaliza

    # Substituições específicas de prefixo
    produto = re.sub(r'^\b(Ca\w*)', 'Café', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Pã\w*)', 'Pão', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Pr\w*)', 'Presunto', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Qu\w*)', 'Queijo', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Pa\w*)', 'Pastel', produto, flags=re.IGNORECASE)
    produto = re.sub(r'^\b(Re\w*)', 'Refri', produto, flags=re.IGNORECASE)

    # Verifica se o produto é um tipo de doce
    if re.search(r'\b(Doce|Doces)\b', produto, flags=re.IGNORECASE):
        # Aqui mantemos o nome do doce específico
        return produto  # Retorna o doce específico como está
    else:
        return produto  # Retorna o produto formatado normalmente

def formatar_produtos(produtos):
    return [formatar_produto(produto) for produto in produtos]

# Exemplo de uso
data = {
    'produtos': ['Doce de leite', 'Café expresso', 'Pão francês', 'Refrigerante', 
                 'Doce de chocolate', 'Bolo de doce', 'Doce com amendoim', 'Doces variados']
}
df = pd.DataFrame(data)

if 'produtos' in df.columns:
    df['produtos'] = formatar_produtos(df['produtos'])

# Criar uma coluna para "Doce (genérico)"
df['doces_genericos'] = df['produtos'].apply(lambda x: 'Doce (genérico)' if 'Doce' in x or 'Doces' in x else x)

# Exibindo o DataFrame atualizado
print(df)
