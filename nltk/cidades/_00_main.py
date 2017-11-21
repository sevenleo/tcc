import time
INICIO = time.time()
# Este arquivo _00_tesy.py

# Chamando os proximos em sequencia de producao:
# Obs. nao vi a necessidade de criar classes

print("\n\n_01_nova_classificacao\n\n")
from _01_nova_classificacao import *

print("\n\n_02_criar_clasificador_postag\n\n")
from _02_criar_clasificador_postag import *

#print("\n\n_03_inserir_novas_frases\n\n")
#from _03_inserir_novas_frases import *

print("\n\n_04_taggear\n\n")
from _04_taggear import *

#print("\n\n_05_check\n\n")
#from _05_check import *

FINAL = time.time()
print(" \n-----------------------------------------\
		\nTEMPO TOTAL: "+str(FINAL - INICIO)+" seg")



###execucao em um intel core i7 2600 com 8GB de ram
###TEMPO TOTAL: 77.31026148796082 seg