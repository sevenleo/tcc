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
    (r"^[nN][ao]s?$", "PRONOME"),
    (r"^[dD][ao]s?$", "PRONOME"),
    (r"^[pP]el[ao]s?$", "PRONOME"),
    (r"^[nN]est[ae]s?$", "PRONOME"),
    (r"^[nN]um$", "PRONOME"),
    (r"^[nN]ess[ae]s?$", "PRONOME"),
    (r"^[nN]aquel[ae]s?$", "PRONOME"),
    (r"^\xe0$", "PRONOME"),
]


tag0 = None
tag1 = None
tag2 = None
tag3 = None
tagf = None
tagr = None
tag0 = nltk.DefaultTagger('__')
tagf = nltk.AffixTagger(train,backoff=tag0)
tag1 = nltk.UnigramTagger(train, backoff=tagf)
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