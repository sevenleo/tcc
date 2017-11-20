#!/usr/bin/env python
# -*- coding: latin-1 -*- 

import pickle
import nltk
import sys

# NOVAS PALAVRAS

insert = []
with open("cidadeslandia.txt", "r") as ins:
	for line in ins:
		line = line.strip()
		#print(line)
		insert.append([(line,"CIDADE")])



regex = [
    (r"^[A-Z0-9._%+-]+\@[A-Z0-9.-]+\.[A-Z]{2,}$", "EMAIL"),
    (r"^[01]?[0-9]\:[012345]\d", "HORA"),
    (r"^[2][0-4]\:[012345]\d", "HORA"),
    (r"\$\d+", "MOEDA"),
    (r"\d+", "NUM"),
]

#TRAIN_STORE
tag0 = nltk.UnigramTagger(insert)
tag  = pickle.load(open('wiki.tag.objb', 'rb')) 
tag1 = nltk.UnigramTagger(insert, backoff=tag)
tag2 = nltk.BigramTagger(insert, backoff=tag1)
tag3 = nltk.TrigramTagger(insert, backoff=tag2)
tagr = nltk.RegexpTagger(regex,backoff=tag3)




def testa_palavra(palavra):
	print(palavra.upper())
	print( "tag0: "	+ 	str(	tag0.tag(	[palavra]	)[0][1]	)	)
	print( " tag: "	+ 	str(	 tag.tag(	[palavra]	)[0][1]	)	)
	print( "tag1: "	+ 	str(	tag1.tag(	[palavra]	)[0][1]	)	)
	print( "tag2: "	+ 	str(	tag2.tag(	[palavra]	)[0][1]	)	)
	print( "tag3: "	+ 	str(	tag3.tag(	[palavra]	)[0][1]	)	)
	print( "tagr: "	+	str(	tagr.tag(	[palavra]	)[0][1]	)	)
	print("\n")


#teste
palavra='rolandia'
testa_palavra(palavra)

palavra='barrolandia'
testa_palavra(palavra)

palavra='landia'
testa_palavra(palavra)
