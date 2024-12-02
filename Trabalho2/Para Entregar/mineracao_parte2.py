import matplotlib.pyplot as plt
import pandas as pd


# df = df.drop(columns=['%'])
# df = df.drop(columns=['Alunos']) # ok
# df = df.drop(column=['Curso'])
# df = df.drop(columns=['Semestre'])

import pandas as pd

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
    # '../D888199_2021-2022.xlsx',
    # '../D888200_2021-2022.xlsx'
]

#Juntando todos os Arquivos em um único DataFrame
dataframes = []
for arquivo in arquivos:
    df = pd.read_excel(arquivo)
    dataframes.append(df)
df  = pd.concat(dataframes, ignore_index=True)

# Removendo colunas Redundantes
df = df.drop(columns=['Cód. Curso'])

# Removendo duplicadas
df = df.drop_duplicates(subset=['Ano','Curso', 'Cód. Disciplina', 'Cód. Turma', 'Situação', 'Semestre'], keep='first')
#Contando numero total de ALunos
df['Tot_Alunos'] = df.groupby(['Ano', 'Curso', 'Cód. Disciplina', 'Cód. Turma', 'Semestre'])['Alunos'].transform('sum')



# Trasnformando Colunas de Reprovacao por Frequencia para somar o total de reprovacoes.
df['Situação'] = df['Situação'].replace({'Repr.Freq': 'Reprovado'})


# Somando com a mesma situacao;
df['Alunos'] = df.groupby(['Ano','Curso', 'Cód. Disciplina', 'Cód. Turma', 'Situação', 'Professor', 'Semestre'])['Alunos'].transform('sum') 

# Pegando apenas alunos reprovados
df_reprovados = df[df['Situação'] == 'Reprovado']

# Removendo duplicadas de Reprovacao
df_reprovados = df_reprovados.drop_duplicates(subset=['Curso', 'Cód. Turma', 'Ano', 'Semestre'], keep='first')
print(df_reprovados)
# print(df) 





resultado = df_reprovados.groupby(['Curso', 'Cód. Disciplina']).agg(
    Total_alunos=('Tot_Alunos', 'sum'),
    Reprovados=('Alunos', 'sum')
).reset_index()

# Calcular a taxa de reprovação como a divisão de Reprovados por Total_alunos
resultado['Taxa_Reprovacao'] = (resultado['Reprovados'] / resultado['Total_alunos']) * 100

# Exibir o resultado ordenado por número de reprovados
resultado_ordenado = resultado.sort_values(by='Cód. Disciplina', ascending=False)

# Exibir o resultado final
print(resultado_ordenado)
input()
