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




print("Carregando base")
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

regular = [
	(r"^cum$", "PREPOSICAO+ARTIGO"),
	(r"^do$", "PREPOSICAO+ARTIGO"),
	(r"^da$", "PREPOSICAO+ARTIGO"),
	(r"^dos$", "PREPOSICAO+ARTIGO"),
	(r"^das$", "PREPOSICAO+ARTIGO"),
	(r"^dum$", "PREPOSICAO+ARTIGO"),
	(r"^duns$", "PREPOSICAO+ARTIGO"),
	(r"^duma$", "PREPOSICAO+ARTIGO"),
	(r"^dumas$", "PREPOSICAO+ARTIGO"),
	(r"^no$", "PREPOSICAO+ARTIGO"),
	(r"^na$", "PREPOSICAO+ARTIGO"),
	(r"^nos$", "PREPOSICAO+ARTIGO"),
	(r"^nas$", "PREPOSICAO+ARTIGO"),
	(r"^num$", "PREPOSICAO+ARTIGO"),
	(r"^nuns$", "PREPOSICAO+ARTIGO"),
	(r"^numa$", "PREPOSICAO+ARTIGO"),
	(r"^numas$", "PREPOSICAO+ARTIGO"),
	(r"^à$", "PREPOSICAO+ARTIGO"),
	(r"^às$", "PREPOSICAO+ARTIGO"),
	(r"^ao$", "PREPOSICAO+ARTIGO"),
	(r"^aos$", "PREPOSICAO+ARTIGO"),
	(r"^dele$", "PREPOSICAO+PRONOME"),
	(r"^dela$", "PREPOSICAO+PRONOME"),
	(r"^deles$", "PREPOSICAO+PRONOME"),
	(r"^delas$", "PREPOSICAO+PRONOME"),
	(r"^deste$", "PREPOSICAO+PRONOME"),
	(r"^desta$", "PREPOSICAO+PRONOME"),
	(r"^destes$", "PREPOSICAO+PRONOME"),
	(r"^destas$", "PREPOSICAO+PRONOME"),
	(r"^disto$", "PREPOSICAO+PRONOME"),
	(r"^desse$", "PREPOSICAO+PRONOME"),
	(r"^dessa$", "PREPOSICAO+PRONOME"),
	(r"^desses$", "PREPOSICAO+PRONOME"),
	(r"^dessas$", "PREPOSICAO+PRONOME"),
	(r"^disso$", "PREPOSICAO+PRONOME"),
	(r"^daquele$", "PREPOSICAO+PRONOME"),
	(r"^daquela$", "PREPOSICAO+PRONOME"),
	(r"^daqueles$", "PREPOSICAO+PRONOME"),
	(r"^daquelas$", "PREPOSICAO+PRONOME"),
	(r"^daquilo$", "PREPOSICAO+PRONOME"),
	(r"^doutro$", "PREPOSICAO+PRONOME"),
	(r"^doutra$", "PREPOSICAO+PRONOME"),
	(r"^doutros$", "PREPOSICAO+PRONOME"),
	(r"^doutra$", "PREPOSICAO+PRONOME"),
	(r"^àquele$", "PREPOSICAO+PRONOME"),
	(r"^àquela$", "PREPOSICAO+PRONOME"),
	(r"^àqueles$", "PREPOSICAO+PRONOME"),
	(r"^àquelas$", "PREPOSICAO+PRONOME"),
	(r"^àquilo$", "PREPOSICAO+PRONOME"),
	(r"^aqueloutro$", "PREPOSICAO+PRONOME"),
	(r"^nele$", "PREPOSICAO+PRONOME"),
	(r"^nela$", "PREPOSICAO+PRONOME"),
	(r"^neles$", "PREPOSICAO+PRONOME"),
	(r"^nelas$", "PREPOSICAO+PRONOME"),
	(r"^neste$", "PREPOSICAO+PRONOME"),
	(r"^nesta$", "PREPOSICAO+PRONOME"),
	(r"^nestes$", "PREPOSICAO+PRONOME"),
	(r"^nestas$", "PREPOSICAO+PRONOME"),
	(r"^nisto$", "PREPOSICAO+PRONOME"),
	(r"^nesse$", "PREPOSICAO+PRONOME"),
	(r"^nessa$", "PREPOSICAO+PRONOME"),
	(r"^nesses$", "PREPOSICAO+PRONOME"),
	(r"^nessas$", "PREPOSICAO+PRONOME"),
	(r"^nisso$", "PREPOSICAO+PRONOME"),
	(r"^naquele$", "PREPOSICAO+PRONOME"),
	(r"^naquela$", "PREPOSICAO+PRONOME"),
	(r"^naqueles$", "PREPOSICAO+PRONOME"),
	(r"^naquelas$", "PREPOSICAO+PRONOME"),
	(r"^naquilo$", "PREPOSICAO+PRONOME"),
	(r"^daqui$", "PREPOSICAO+ADVERBIO"),
	(r"^daí$", "PREPOSICAO+ADVERBIO"),
	(r"^dai$", "PREPOSICAO+ADVERBIO"),
	(r"^dali$", "PREPOSICAO+ADVERBIO"),
	(r"^dalém$", "PREPOSICAO+ADVERBIO"),
	(r"^dalem$", "PREPOSICAO+ADVERBIO"),
	(r"^aonde$", "PREPOSICAO+ADVERBIO"),
	(r"^donde$", "PREPOSICAO+ADVERBIO"),
    (r"^[nN][ao]s?$", "PREPOSICAO+PRONOME"),
    (r"^[dD][ao]s?$", "PREPOSICAO+PRONOME"),
    (r"^[pP]el[ao]s?$", "PREPOSICAO+PRONOME"),
    (r"^[nN]est[ae]s?$", "PREPOSICAO+PRONOME"),
    (r"^[nN]um$", "PREPOSICAO+PRONOME"),
    (r"^[nN]ess[ae]s?$", "PREPOSICAO+PRONOME"),
    (r"^[nN]aquel[ae]s?$", "PREPOSICAO+PRONOME"),
    (r"^\xe0$", "PREPOSICAO+"),
]


tag0 = None
tag1 = None
tag2 = None
tag3 = None
tagf = None
tagr = None
tag0 = nltk.DefaultTagger('__')
#tagf = nltk.AffixTagger(train,backoff=tag0)
tag1 = nltk.UnigramTagger(train, backoff=tag0)
tagr = nltk.RegexpTagger(regular, backoff=tag1)
tag2 = nltk.BigramTagger(train, backoff=tagr)
tag3 = nltk.TrigramTagger(train, backoff=tag2)

#templates = nltk.brill.fntbl37()
#tagger = nltk.BrillTaggerTrainer(tagger, templates)
#tagger = tagger.train(traindata, max_rules=100)

tag=tag3


print("Verificando acuracia")
#https://streamhacker.com/2008/11/03/part-of-speech-tagging-with-nltk-part-1/
#verficar a precisao no NLTK
#nltk.tag.accuracy(tag, test)
#verficar a precisao no NLTK 2.0
#tag.evaluate(test)




#SAVE TRAIN FILE
filename = 'wiki.tag.obj'
print("Salvando arquivo "+filename)
file_tag = open(filename, 'w') 
pickle.dump(tag, file_tag) 




print("Base finalizada")