# Tabelas
import pandas as pd


nomes = ["Steve", "Bill", "Martin"]
literatura = [8.5, 9, 10]
matematica = [9, 9.5, 7]

#1 - Cria a tabela 
DF1 = pd.DataFrame({
    'Nome': nomes,
    'Literatura': literatura,
    'Matemática': matematica
})
print(DF1)
print()

#2 - Crie a tabela com disciplina
DF2 = pd.DataFrame({
    'Disciplina': ['Literatura', 'Matematica'],
    'Steve': [literatura[0], matematica[0]],
    'Bill': [literatura[1], matematica[1]],
    'Martin': [literatura[2], matematica[2]]
})
print(DF2)
print()


DF3 = pd.DataFrame({

    'Nome': nomes * 2,
    'Disciplina': ['literatura']*3 + ['Matematica']*3,
    'Nota': literatura + matematica
})

print(DF3)