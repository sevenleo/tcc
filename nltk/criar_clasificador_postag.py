#!/usr/bin/env python
# -*- coding: latin-1 -*- 

print("Incializando")
#import unidecode
#unaccented_string = unidecode.unidecode(txt)
import pickle
import nltk
import json
from nltk.corpus import mac_morpho, stopwords
lang = 'portuguese'




print("Carregango base")
#train = mac_morpho.tagged_sents()
#train = nltk.corpus.floresta.tagged_sents()
json_data=open('wiki.json').read()
train = json.loads(json_data)




print("Separando arquivos test/treino")
#train = mac_morpho.tagged_sents()[100:]
#test = mac_morpho.tagged_sents()[:100]




print("Treinando taggers")
# http://nlpforhackers.io/training-pos-tagger/
# DefaultTagger that simply tags everything with the same tag
# RegexpTagger that applies tags according to a set of regular expressions
# UnigramTagger that picks the most frequent tag for a known word
# BigramTagger, TrigramTagger working similarly to the UnigramTagger but also taking some of the context into consideration
tag0 = None
tag1 = None
tag2 = None
tag3 = None
tag0 = nltk.DefaultTagger('__')
tag1 = nltk.UnigramTagger(train, backoff=tag0)
tag2 = nltk.BigramTagger(train, backoff=tag1)
tag3 = nltk.TrigramTagger(train, backoff=tag2)




print("Verificando acuracia")
#https://streamhacker.com/2008/11/03/part-of-speech-tagging-with-nltk-part-1/
#verficar a precisao no NLTK
#nltk.tag.accuracy(tag3, test)
#verficar a precisao no NLTK 2.0
#tag3.evaluate(test)




#SAVE TRAIN FILE
filename = 'wiki.tag3.obj'
print("Salvando arquivo "+filename)
file_tag3 = open(filename, 'w') 
pickle.dump(tag3, file_tag3) 




print("Base finalizada")