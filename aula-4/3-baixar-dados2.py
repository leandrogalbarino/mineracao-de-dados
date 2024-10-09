import urllib.request

# URL do arquivo que você deseja baixar
arqUrl = "https://www-usr.inf.ufsm.br/~joaquim/UFSM/DM/ds/Insetos00.csv"

# Nome do arquivo de destino (destfile)
destFile = "./aula-4/test2.csv"

# Fazendo o download do arquivo
urllib.request.urlretrieve(arqUrl, destFile)

print(f"Arquivo baixado e salvo em: {destFile}")
