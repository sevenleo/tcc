from nltk.corpus import mac_morpho, floresta, stopwords
import sys
#for param in sys.argv :
#    print(param)

buscar=sys.argv[1].decode('utf-8')
rev=sys.argv[2]
print ('\nbuscar:')
print (buscar)
print('\nscan:')
print(rev)


if sys.argv[0] == "":
	buscar = "AP".lower()

if rev == "m":
	print("carregando mac_morpho")
	print("pesquisando em mac_morpho ...")
	m = mac_morpho.tagged_sents()
	for t in m:
		for w in t:
			if buscar is w[1].lower():
				print(w)
elif rev == "f":
	print("carregando floresta")
	print("pesquisando em floresta ...")
	f = floresta.tagged_sents()
	for t in f:
		for w in t:
			if buscar is w[1].lower():
				print(w)
else:
	print("carregando mac_morpho")
	print("pesquisando em mac_morpho ...")
	m = mac_morpho.tagged_sents()
	for t in m:
		for w in t:
			if buscar is w[1].lower():
				print(w)

	print("carregando floresta")
	print("pesquisando em floresta ...")
	f = floresta.tagged_sents()
	for t in f:
		for w in t:
			if buscar is w[1].lower():
				print(w)
