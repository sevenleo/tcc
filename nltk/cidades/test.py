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
tag = pickle.load(open('wiki.tag.objb', 'rb')) 
tag0 = nltk.UnigramTagger(insert)
#tag0 = nltk.DefaultTagger('__')
tag1 = nltk.UnigramTagger(insert, backoff=tag0)
tag2 = nltk.BigramTagger(insert, backoff=tag1)
tag3 = nltk.TrigramTagger(insert, backoff=tag2)
tagr = nltk.RegexpTagger(regex,backoff=tag3)





#teste
palavra='rolandia'
print( " tag: "	+ 	str(	 tag.tag(	[palavra]	)	)	)
print( "tag0: "	+ 	str(	tag0.tag(	[palavra]	)	)	)
print( "tag1: "	+ 	str(	tag1.tag(	[palavra]	)	)	)
print( "tag2: "	+ 	str(	tag2.tag(	[palavra]	)	)	)
print( "tag3: "	+ 	str(	tag3.tag(	[palavra]	)	)	)
print( "tagr: "	+	str(	tagr.tag(	[palavra]	)	)	)

palavra='barrolandia'
print( " tag: "	+ 	str(	 tag.tag(	[palavra]	)	)	)
print( "tag0: "	+ 	str(	tag0.tag(	[palavra]	)	)	)
print( "tag1: "	+ 	str(	tag1.tag(	[palavra]	)	)	)
print( "tag2: "	+ 	str(	tag2.tag(	[palavra]	)	)	)
print( "tag3: "	+ 	str(	tag3.tag(	[palavra]	)	)	)
print( "tagr: "	+	str(	tagr.tag(	[palavra]	)	)	)

palavra='barolandia'
print( " tag: "	+ 	str(	 tag.tag(	[palavra]	)	)	)
print( "tag0: "	+ 	str(	tag0.tag(	[palavra]	)	)	)
print( "tag1: "	+ 	str(	tag1.tag(	[palavra]	)	)	)
print( "tag2: "	+ 	str(	tag2.tag(	[palavra]	)	)	)
print( "tag3: "	+ 	str(	tag3.tag(	[palavra]	)	)	)
print( "tagr: "	+	str(	tagr.tag(	[palavra]	)	)	)