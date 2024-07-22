import os

# Caminho da pasta que queremos verificar
caminho_pasta = '../../clueweb09-pt'

# Verifica se a pasta existe
if os.path.exists(caminho_pasta) and os.path.isdir(caminho_pasta):
    print(f"A pasta '{caminho_pasta}' existe.")
    
    # Lista os arquivos dentro da pasta
    arquivos = os.listdir(caminho_pasta)
    
    if arquivos:
        print("Arquivos na pasta:")
        for arquivo in arquivos:
            print(arquivo)
    else:
        print("A pasta está vazia.")
else:
    print(f"A pasta '{caminho_pasta}' não existe.")
