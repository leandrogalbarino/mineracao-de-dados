import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def cursos_maior_taxa_reprovacao(resultado):
    resultado_ordenado = resultado.sort_values(by='Taxa_Reprovacao', ascending=False)
    pd.options.display.float_format = '{:,.2f}'.format
    # print(resultado_ordenado)
    print(f"Top 15 Cursos que tiveram mais dificuldade realizando a Disciplina:")
    print(resultado_ordenado.head(15))

def grafico_taxa_reprovacao(resultado):
    # Criar um DataFrame Pivot para facilitar a visualização
    pivot_df = resultado.pivot(index='Curso', columns='Cód. Disciplina', values='Taxa_Reprovacao')

    # Configurar o tamanho do gráfico

    # Criar gráfico de barras empilhadas
    pivot_df.plot(kind='bar', stacked=False, figsize=(8, 6), colormap='tab20')

    # Adicionar títulos e rótulos
    plt.title('Taxa de Reprovação por Curso e Disciplina', fontsize=14)
    plt.xlabel('Cursos', fontsize=12)
    plt.ylabel('Taxa de Reprovação (%)', fontsize=12)
    plt.legend(title='Cód. Disciplina', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.ylim(0, 100)

    # Ajustar layout para melhor exibição
    plt.tight_layout()

    # Mostrar gráfico
    plt.show()

def disciplinas_mais_reprovadas(resultado):
    resultado_disciplina = resultado.groupby('Cód. Disciplina').agg(
        Total_Reprovados=('Reprovados', 'sum'),
        Media_Taxa_Reprovacao=('Taxa_Reprovacao', 'mean')
    ).sort_values(by='Total_Reprovados', ascending=False).reset_index()

    print("\nTop 10 Disciplinas com maior número de reprovações:")
    print(resultado_disciplina.head(10))
    
    return resultado_disciplina

def regras_de_associacao():
    pd.set_option('future.no_silent_downcasting', True)
    limiar_reprovacao = 50  # Pode ajustar conforme necessário

    # Criar tabela binária: 1 para disciplinas com taxa de reprovação acima do limiar
    resultado['Alta_Reprovacao'] = resultado['Taxa_Reprovacao'] > limiar_reprovacao

    # Criar a matriz binária para Apriori
    df_transacoes = resultado.pivot(index='Curso', columns='Cód. Disciplina', values='Alta_Reprovacao').fillna(False)
    df_transacoes = df_transacoes.astype(bool)  # Garantir que os valores sejam booleanos



    print(df_transacoes)
    # Aplicar o algoritmo Apriori
    frequent_itemsets = apriori(df_transacoes, min_support=0.02, use_colnames=True)

    frequent_itemsets['num_items'] = frequent_itemsets['itemsets'].apply(len)

    # Gerar regras de associação com o novo parâmetro
    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=1.2,
        num_itemsets=frequent_itemsets['num_items']
    )

    # Filtrar e exibir regras relevantes
    rules_sorted = rules.sort_values(by='lift', ascending=False)
    print("\nRegras de Associação:")
    print(rules_sorted[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

    # Filtrar regras relevantes
    rules_filtered = rules[rules['confidence'] > 0.6]
    print("Regras relevantes para disciplinas problemáticas:")
    print(rules_filtered[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# Lista de arquivos Excel com as mesmas colunas
arquivos = [
    '../D200888_2021.xlsx',
    '../D200888_2022.xlsx',
    '../D200888_2023.xlsx',
    '../D320200_2021-2022.xlsx',
    '../D402855_2021.xlsx',
    '../D402855_2022.xlsx',
    '../D402855_2023.xlsx',
    '../D888148_2021.xlsx',
    '../D888148_2022.xlsx',
    '../D888148_2023.xlsx',
    '../D888199_2021-2022.xlsx',
    '../D888200_2021-2022.xlsx',
]

#Juntando todos os Arquivos em um único DataFrame
dataframes = []
for arquivo in arquivos:
    try:
        df = pd.read_excel(arquivo)
        dataframes.append(df)
        print(f"Arquivo carregado: {arquivo}")
    except Exception as e:
        print(f"Erro ao carregar {arquivo}: {e}")

df  = pd.concat(dataframes, ignore_index=True)

# Removendo colunas Redundantes
if 'Cód. Curso' in df.columns:
    df = df.drop(columns=['Cód. Curso'])
if 'Professor' in df.columns:
    df = df.drop(columns=['Professor'])
if '%' in df.columns:
    df = df.drop(columns=['%'])

df['Alunos'] = pd.to_numeric(df['Alunos'], errors='coerce')

# Removendo duplicadas geradas por turmas com mais de um professor
df = df.drop_duplicates(subset=['Ano','Curso', 'Cód. Disciplina', 'Cód. Turma', 'Situação', 'Semestre'], keep='first')


# Somando o numero de Alunos na Disciplina para utilizar quando for calcular a porcentagem de reprovacao total
df['Tot_Alunos'] = df.groupby(['Ano', 'Curso', 'Cód. Disciplina', 'Cód. Turma', 'Semestre'])['Alunos'].transform('sum')

# # Trasnformando Colunas de Reprovacao por Frequencia para somar o total de reprovacoes.
df['Situação'] = df['Situação'].replace({'Repr.Freq': 'Reprovado'})

# Somando com a mesma situacao;
df['Alunos'] = df.groupby(['Ano','Curso', 'Cód. Disciplina', 'Cód. Turma', 'Situação', 'Semestre'])['Alunos'].transform('sum') 

# Removendo coluna duplicada, gerada pela transformacao de Repr. Freq para Reprovado
df = df.drop_duplicates(subset=['Ano','Curso', 'Cód. Disciplina', 'Cód. Turma', 'Situação', 'Semestre'], keep='first')

# print(df)

# # Pegando apenas alunos reprovados
df_reprovados = df[df['Situação'] == 'Reprovado']

# # Removendo duplicadas de Reprovacao

resultado = df_reprovados.groupby(['Curso', 'Cód. Disciplina']).agg(
    Total_alunos=('Tot_Alunos', 'sum'),
    Reprovados=('Alunos', 'sum')
).reset_index()

# # Calcular a taxa de reprovação como a divisão de Reprovados por Total_alunos
resultado['Taxa_Reprovacao'] = (resultado['Reprovados'] / resultado['Total_alunos']).replace([float('inf'), float('nan')], 0) * 100

# # Exibir o resultado ordenado por número de reprovados
print(resultado)

cursos_maior_taxa_reprovacao(resultado)
grafico_taxa_reprovacao(resultado) 
regras_de_associacao(resultado)


input()
