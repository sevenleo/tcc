from _00_functions import *



try:
	file = str(sys.argv[1])
except:
	file = 'pt'
lang = 'pt'

erros = 0


#LOAD FILES
try:
	loadfilename = 'W2V'+'/'+file+'.model'
	logs("LOAD FILE (model)",loadfilename)
	w2v = Word2Vec.load(loadfilename)
	print("FILE LOADED")
except:
	print(file+".model FILE NOT EXIST")
	w2v = loadfromfile('W2V',file,'W2V')
	exit()

size(w2v)

args = sys.argv

if len(sys.argv) < 3:
	print("\nERRO\n")
	print("Exemplo de uso:")
	print("python check.py modelo termo1 termo2 termo3 ...")
else:
	lang = args[1]
	print("\n")
	for arg in args:
		if args.index(arg) == 0 or args.index(arg) == 1:
			continue
		predicts,similares,erros = checkinmodel(w2v,arg,erros)