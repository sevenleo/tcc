from _00_functions import *
import sys
args = sys.argv


if len(sys.argv) < 3:
	print("\nERRO\n")
	print("Exemplo de uso:")
	print("python search.py idioma termo1 termo2 termo3 ...")
else:
	lang = args[1]
	print("\n")
	print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	print("searching elements ...\n")
	for arg in args:
		if args.index(arg) == 0 or args.index(arg) == 1:
			continue
		print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
		print( args.index(arg), ':', arg )
		print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
		text = search(arg)
		save_txt_to_file(arg,lang,text)


