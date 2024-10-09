import os

diretorio_atual = os.getcwd()
print(f"Diretório de trabalho atual: {diretorio_atual}")

# Diretório absoluto
novo_diretorio = 'C:\\Users\\leand\\OneDrive\\Documentos\\meus-projetos\\algoritmos-python\\mineracao-dados\\aula-4'
os.chdir(novo_diretorio)
print(f"Diretório de trabalho atual: {os.getcwd()}")

# Diretório relativo
novo_diretorio = '../'
os.chdir(novo_diretorio)
print(f"Diretório de trabalho atual: {os.getcwd()}")

nome_diretorio = "aula-4/diretorio1/diretorio2"

# Verificar se o diretório existe (equivalente ao file.exists() em R)
if os.path.exists(nome_diretorio):
    print(f"O diretório '{nome_diretorio}' já existe!")
else:
    print(f"O diretório '{nome_diretorio}' não existe!")

# Criar o diretório (equivalente ao dir.create() em R)
if not os.path.exists(nome_diretorio):
    os.makedirs(nome_diretorio)
    print(f"O repotório '{nome_diretorio}' foi criado com sucesso!")
else:
    print(f"O repositório '{nome_diretorio}' já existe!")