#!/usr/bin/env python
# -*- coding: latin-1 -*- 

#import unidecode
#unaccented_string = unidecode.unidecode(txt)
import pickle
import nltk
from nltk.corpus import mac_morpho, stopwords





lang = 'portuguese'
train = mac_morpho.tagged_sents()
#train = nltk.corpus.floresta.tagged_sents()

#train = mac_morpho.tagged_sents()[100:]
#test = mac_morpho.tagged_sents()[:100]






# http://nlpforhackers.io/training-pos-tagger/
# DefaultTagger that simply tags everything with the same tag
# RegexpTagger that applies tags according to a set of regular expressions
# UnigramTagger that picks the most frequent tag for a known word
# BigramTagger, TrigramTagger working similarly to the UnigramTagger but also taking some of the context into consideration
tag0 = None
tag1 = None
tag2 = None
tag3 = None
tag0 = nltk.DefaultTagger('unk')
tag1 = nltk.UnigramTagger(train, backoff=tag0)
tag2 = nltk.BigramTagger(train, backoff=tag1)
tag3 = nltk.TrigramTagger(train, backoff=tag2)





#https://streamhacker.com/2008/11/03/part-of-speech-tagging-with-nltk-part-1/
#verficar a precisao no NLTK
#nltk.tag.accuracy(tag3, test)
#verficar a precisao no NLTK 2.0
#tag3.evaluate(test)


'''
#ADICONAR ESTES TREINOS
# nltk.corpus.mac_morpho.tagged_sents is incorrect, converting tagged_paras to tagged_sents
dataset1 = list(nltk.corpus.floresta.tagged_sents())
dataset2 = [[w[0] for w in sent] for sent in nltk.corpus.mac_morpho.tagged_paras()]
'''


'''
#ADICIONAR LISTA PALAVRAS MANUALMENTE
	palavras desconhecidas (unk) devem ser adicionadas manualmente
	devemos treinar novamente
	adicionar as palavras:
		(S~ao,Verbo)
		(ideia,substantivo)
	adicionar esta linha ao codigo, antes de treinar com o nltk..Tagger:
		tam=lenght(train)]
		train[tam].append(["sao",V])
		train[tam].append(["sao",V])
	Mas a melhor forma de obter a classificacao ´e, criar uma lista de palavras desconhecidas apos varias classificacoes e procura-las em dicionarios reais
'''




#SAVE TRAIN FILE
file_tag3 = open('tag3_mac.obj', 'w') 
pickle.dump(tag3, file_tag3) 
