import requests

# URL do arquivo que você deseja baixar
arqUrl = "https://www-usr.inf.ufsm.br/~joaquim/UFSM/DM/ds/Insetos00.csv"

# Nome do arquivo de destino (destfile)
destFile = "./aula-4/test.csv"

# Fazendo o download do arquivo
response = requests.get(arqUrl) 

# Salvando o conteúdo no arquivo local
with open(destFile, 'wb') as file:
    file.write(response.content)

print(f"Arquivo baixado e salvo em: {destFile}")
