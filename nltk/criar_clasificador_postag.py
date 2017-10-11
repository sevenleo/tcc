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
test = mac_morpho.tagged_sents()[:100]




print("Treinando taggers")
# http://nlpforhackers.io/training-pos-tagger/
# DefaultTagger that simply tags everything with the same tag
# RegexpTagger that applies tags according to a set of regular expressions
# UnigramTagger that picks the most frequent tag for a known word
# BigramTagger, TrigramTagger working similarly to the UnigramTagger but also taking some of the context into consideration

regular = [

	(r'(cum)$', 'PREPOSICAO+ARTIGO'),
	(r'(do)$', 'PREPOSICAO+ARTIGO'),
	(r'(da)$', 'PREPOSICAO+ARTIGO'),
	(r'(dos)$', 'PREPOSICAO+ARTIGO'),
	(r'(das)$', 'PREPOSICAO+ARTIGO'),
	(r'(dum)$', 'PREPOSICAO+ARTIGO'),
	(r'(duns)$', 'PREPOSICAO+ARTIGO'),
	(r'(duma)$', 'PREPOSICAO+ARTIGO'),
	(r'(dumas)$', 'PREPOSICAO+ARTIGO'),
	(r'(no)$', 'PREPOSICAO+ARTIGO'),
	(r'(na)$', 'PREPOSICAO+ARTIGO'),
	(r'(nos)$', 'PREPOSICAO+ARTIGO'),
	(r'(nas)$', 'PREPOSICAO+ARTIGO'),
	(r'(num)$', 'PREPOSICAO+ARTIGO'),
	(r'(nuns)$', 'PREPOSICAO+ARTIGO'),
	(r'(numa)$', 'PREPOSICAO+ARTIGO'),
	(r'(numas)$', 'PREPOSICAO+ARTIGO'),
	(r'(à)$', 'PREPOSICAO+ARTIGO'),
	(r'(às)$', 'PREPOSICAO+ARTIGO'),
	(r'(ao)$', 'PREPOSICAO+ARTIGO'),
	(r'(aos)$', 'PREPOSICAO+ARTIGO'),
	(r'(dele)$', 'PREPOSICAO+PRONOME'),
	(r'(dela)$', 'PREPOSICAO+PRONOME'),
	(r'(deles)$', 'PREPOSICAO+PRONOME'),
	(r'(delas)$', 'PREPOSICAO+PRONOME'),
	(r'(deste)$', 'PREPOSICAO+PRONOME'),
	(r'(desta)$', 'PREPOSICAO+PRONOME'),
	(r'(destes)$', 'PREPOSICAO+PRONOME'),
	(r'(destas)$', 'PREPOSICAO+PRONOME'),
	(r'(disto)$', 'PREPOSICAO+PRONOME'),
	(r'(desse)$', 'PREPOSICAO+PRONOME'),
	(r'(dessa)$', 'PREPOSICAO+PRONOME'),
	(r'(desses)$', 'PREPOSICAO+PRONOME'),
	(r'(dessas)$', 'PREPOSICAO+PRONOME'),
	(r'(disso)$', 'PREPOSICAO+PRONOME'),
	(r'(daquele)$', 'PREPOSICAO+PRONOME'),
	(r'(daquela)$', 'PREPOSICAO+PRONOME'),
	(r'(daqueles)$', 'PREPOSICAO+PRONOME'),
	(r'(daquelas)$', 'PREPOSICAO+PRONOME'),
	(r'(daquilo)$', 'PREPOSICAO+PRONOME'),
	(r'(doutro)$', 'PREPOSICAO+PRONOME'),
	(r'(doutra)$', 'PREPOSICAO+PRONOME'),
	(r'(doutros)$', 'PREPOSICAO+PRONOME'),
	(r'(doutra)$', 'PREPOSICAO+PRONOME'),
	(r'(àquele)$', 'PREPOSICAO+PRONOME'),
	(r'(àquela)$', 'PREPOSICAO+PRONOME'),
	(r'(àqueles)$', 'PREPOSICAO+PRONOME'),
	(r'(àquelas)$', 'PREPOSICAO+PRONOME'),
	(r'(àquilo)$', 'PREPOSICAO+PRONOME'),
	(r'(aqueloutro)$', 'PREPOSICAO+PRONOME'),
	(r'(nele)$', 'PREPOSICAO+PRONOME'),
	(r'(nela)$', 'PREPOSICAO+PRONOME'),
	(r'(neles)$', 'PREPOSICAO+PRONOME'),
	(r'(nelas)$', 'PREPOSICAO+PRONOME'),
	(r'(neste)$', 'PREPOSICAO+PRONOME'),
	(r'(nesta)$', 'PREPOSICAO+PRONOME'),
	(r'(nestes)$', 'PREPOSICAO+PRONOME'),
	(r'(nestas)$', 'PREPOSICAO+PRONOME'),
	(r'(nisto)$', 'PREPOSICAO+PRONOME'),
	(r'(nesse)$', 'PREPOSICAO+PRONOME'),
	(r'(nessa)$', 'PREPOSICAO+PRONOME'),
	(r'(nesses)$', 'PREPOSICAO+PRONOME'),
	(r'(nessas)$', 'PREPOSICAO+PRONOME'),
	(r'(nisso)$', 'PREPOSICAO+PRONOME'),
	(r'(naquele)$', 'PREPOSICAO+PRONOME'),
	(r'(naquela)$', 'PREPOSICAO+PRONOME'),
	(r'(naqueles)$', 'PREPOSICAO+PRONOME'),
	(r'(naquelas)$', 'PREPOSICAO+PRONOME'),
	(r'(naquilo)$', 'PREPOSICAO+PRONOME'),
	(r'(daqui)$', 'PREPOSICAO+ADVERBIO'),
	(r'(daí)$', 'PREPOSICAO+ADVERBIO'),
	(r'(dai)$', 'PREPOSICAO+ADVERBIO'),
	(r'(dali)$', 'PREPOSICAO+ADVERBIO'),
	(r'(dalém)$', 'PREPOSICAO+ADVERBIO'),
	(r'(dalem)$', 'PREPOSICAO+ADVERBIO'),
	(r'(aonde)$', 'PREPOSICAO+ADVERBIO'),
	(r'(donde)$', 'PREPOSICAO+ADVERBIO'),


	(r'(CUM)$', 'PREPOSICAO+ARTIGO'),
	(r'(DO)$', 'PREPOSICAO+ARTIGO'),
	(r'(DA)$', 'PREPOSICAO+ARTIGO'),
	(r'(DOS)$', 'PREPOSICAO+ARTIGO'),
	(r'(DAS)$', 'PREPOSICAO+ARTIGO'),
	(r'(DUM)$', 'PREPOSICAO+ARTIGO'),
	(r'(DUNS)$', 'PREPOSICAO+ARTIGO'),
	(r'(DUMA)$', 'PREPOSICAO+ARTIGO'),
	(r'(DUMAS)$', 'PREPOSICAO+ARTIGO'),
	(r'(NO)$', 'PREPOSICAO+ARTIGO'),
	(r'(NA)$', 'PREPOSICAO+ARTIGO'),
	(r'(NOS)$', 'PREPOSICAO+ARTIGO'),
	(r'(NAS)$', 'PREPOSICAO+ARTIGO'),
	(r'(NUM)$', 'PREPOSICAO+ARTIGO'),
	(r'(NUNS)$', 'PREPOSICAO+ARTIGO'),
	(r'(NUMA)$', 'PREPOSICAO+ARTIGO'),
	(r'(NUMAS)$', 'PREPOSICAO+ARTIGO'),
	(r'(À)$', 'PREPOSICAO+ARTIGO'),
	(r'(ÀS)$', 'PREPOSICAO+ARTIGO'),
	(r'(AO)$', 'PREPOSICAO+ARTIGO'),
	(r'(AOS)$', 'PREPOSICAO+ARTIGO'),
	(r'(DELE)$', 'PREPOSICAO+PRONOME'),
	(r'(DELA)$', 'PREPOSICAO+PRONOME'),
	(r'(DELES)$', 'PREPOSICAO+PRONOME'),
	(r'(DELAS)$', 'PREPOSICAO+PRONOME'),
	(r'(DESTE)$', 'PREPOSICAO+PRONOME'),
	(r'(DESTA)$', 'PREPOSICAO+PRONOME'),
	(r'(DESTES)$', 'PREPOSICAO+PRONOME'),
	(r'(DESTAS)$', 'PREPOSICAO+PRONOME'),
	(r'(DISTO)$', 'PREPOSICAO+PRONOME'),
	(r'(DESSE)$', 'PREPOSICAO+PRONOME'),
	(r'(DESSA)$', 'PREPOSICAO+PRONOME'),
	(r'(DESSES)$', 'PREPOSICAO+PRONOME'),
	(r'(DESSAS)$', 'PREPOSICAO+PRONOME'),
	(r'(DISSO)$', 'PREPOSICAO+PRONOME'),
	(r'(DAQUELE)$', 'PREPOSICAO+PRONOME'),
	(r'(DAQUELA)$', 'PREPOSICAO+PRONOME'),
	(r'(DAQUELES)$', 'PREPOSICAO+PRONOME'),
	(r'(DAQUELAS)$', 'PREPOSICAO+PRONOME'),
	(r'(DAQUILO)$', 'PREPOSICAO+PRONOME'),
	(r'(DOUTRO)$', 'PREPOSICAO+PRONOME'),
	(r'(DOUTRA)$', 'PREPOSICAO+PRONOME'),
	(r'(DOUTROS)$', 'PREPOSICAO+PRONOME'),
	(r'(DOUTRA)$', 'PREPOSICAO+PRONOME'),
	(r'(ÀQUELE)$', 'PREPOSICAO+PRONOME'),
	(r'(ÀQUELA)$', 'PREPOSICAO+PRONOME'),
	(r'(ÀQUELES)$', 'PREPOSICAO+PRONOME'),
	(r'(ÀQUELAS)$', 'PREPOSICAO+PRONOME'),
	(r'(ÀQUILO)$', 'PREPOSICAO+PRONOME'),
	(r'(AQUELOUTRO)$', 'PREPOSICAO+PRONOME'),
	(r'(NELE)$', 'PREPOSICAO+PRONOME'),
	(r'(NELA)$', 'PREPOSICAO+PRONOME'),
	(r'(NELES)$', 'PREPOSICAO+PRONOME'),
	(r'(NELAS)$', 'PREPOSICAO+PRONOME'),
	(r'(NESTE)$', 'PREPOSICAO+PRONOME'),
	(r'(NESTA)$', 'PREPOSICAO+PRONOME'),
	(r'(NESTES)$', 'PREPOSICAO+PRONOME'),
	(r'(NESTAS)$', 'PREPOSICAO+PRONOME'),
	(r'(NISTO)$', 'PREPOSICAO+PRONOME'),
	(r'(NESSE)$', 'PREPOSICAO+PRONOME'),
	(r'(NESSA)$', 'PREPOSICAO+PRONOME'),
	(r'(NESSES)$', 'PREPOSICAO+PRONOME'),
	(r'(NESSAS)$', 'PREPOSICAO+PRONOME'),
	(r'(NISSO)$', 'PREPOSICAO+PRONOME'),
	(r'(NAQUELE)$', 'PREPOSICAO+PRONOME'),
	(r'(NAQUELA)$', 'PREPOSICAO+PRONOME'),
	(r'(NAQUELES)$', 'PREPOSICAO+PRONOME'),
	(r'(NAQUELAS)$', 'PREPOSICAO+PRONOME'),
	(r'(NAQUILO)$', 'PREPOSICAO+PRONOME'),
	(r'(DAQUI)$', 'PREPOSICAO+ADVERBIO'),
	(r'(DAÍ)$', 'PREPOSICAO+ADVERBIO'),
	(r'(DAI)$', 'PREPOSICAO+ADVERBIO'),
	(r'(DALI)$', 'PREPOSICAO+ADVERBIO'),
	(r'(DALÉM)$', 'PREPOSICAO+ADVERBIO'),
	(r'(DALEM)$', 'PREPOSICAO+ADVERBIO'),
	(r'(AONDE)$', 'PREPOSICAO+ADVERBIO'),
	(r'(DONDE)$', 'PREPOSICAO+ADVERBIO'),

		(r'(Cum)$', 'PREPOSICAO+ARTIGO'),
	(r'(Do)$', 'PREPOSICAO+ARTIGO'),
	(r'(Da)$', 'PREPOSICAO+ARTIGO'),
	(r'(Dos)$', 'PREPOSICAO+ARTIGO'),
	(r'(Das)$', 'PREPOSICAO+ARTIGO'),
	(r'(Dum)$', 'PREPOSICAO+ARTIGO'),
	(r'(Duns)$', 'PREPOSICAO+ARTIGO'),
	(r'(Duma)$', 'PREPOSICAO+ARTIGO'),
	(r'(Dumas)$', 'PREPOSICAO+ARTIGO'),
	(r'(No)$', 'PREPOSICAO+ARTIGO'),
	(r'(Na)$', 'PREPOSICAO+ARTIGO'),
	(r'(Nos)$', 'PREPOSICAO+ARTIGO'),
	(r'(Nas)$', 'PREPOSICAO+ARTIGO'),
	(r'(Num)$', 'PREPOSICAO+ARTIGO'),
	(r'(Nuns)$', 'PREPOSICAO+ARTIGO'),
	(r'(Numa)$', 'PREPOSICAO+ARTIGO'),
	(r'(Numas)$', 'PREPOSICAO+ARTIGO'),
	(r'(À)$', 'PREPOSICAO+ARTIGO'),
	(r'(Às)$', 'PREPOSICAO+ARTIGO'),
	(r'(Ao)$', 'PREPOSICAO+ARTIGO'),
	(r'(Aos)$', 'PREPOSICAO+ARTIGO'),
	(r'(Dele)$', 'PREPOSICAO+PRONOME'),
	(r'(Dela)$', 'PREPOSICAO+PRONOME'),
	(r'(Deles)$', 'PREPOSICAO+PRONOME'),
	(r'(Delas)$', 'PREPOSICAO+PRONOME'),
	(r'(Deste)$', 'PREPOSICAO+PRONOME'),
	(r'(Desta)$', 'PREPOSICAO+PRONOME'),
	(r'(Destes)$', 'PREPOSICAO+PRONOME'),
	(r'(Destas)$', 'PREPOSICAO+PRONOME'),
	(r'(Disto)$', 'PREPOSICAO+PRONOME'),
	(r'(Desse)$', 'PREPOSICAO+PRONOME'),
	(r'(Dessa)$', 'PREPOSICAO+PRONOME'),
	(r'(Desses)$', 'PREPOSICAO+PRONOME'),
	(r'(Dessas)$', 'PREPOSICAO+PRONOME'),
	(r'(Disso)$', 'PREPOSICAO+PRONOME'),
	(r'(Daquele)$', 'PREPOSICAO+PRONOME'),
	(r'(Daquela)$', 'PREPOSICAO+PRONOME'),
	(r'(Daqueles)$', 'PREPOSICAO+PRONOME'),
	(r'(Daquelas)$', 'PREPOSICAO+PRONOME'),
	(r'(Daquilo)$', 'PREPOSICAO+PRONOME'),
	(r'(Doutro)$', 'PREPOSICAO+PRONOME'),
	(r'(Doutra)$', 'PREPOSICAO+PRONOME'),
	(r'(Doutros)$', 'PREPOSICAO+PRONOME'),
	(r'(Doutra)$', 'PREPOSICAO+PRONOME'),
	(r'(Àquele)$', 'PREPOSICAO+PRONOME'),
	(r'(Àquela)$', 'PREPOSICAO+PRONOME'),
	(r'(Àqueles)$', 'PREPOSICAO+PRONOME'),
	(r'(Àquelas)$', 'PREPOSICAO+PRONOME'),
	(r'(Àquilo)$', 'PREPOSICAO+PRONOME'),
	(r'(Aqueloutro)$', 'PREPOSICAO+PRONOME'),
	(r'(Nele)$', 'PREPOSICAO+PRONOME'),
	(r'(Nela)$', 'PREPOSICAO+PRONOME'),
	(r'(Neles)$', 'PREPOSICAO+PRONOME'),
	(r'(Nelas)$', 'PREPOSICAO+PRONOME'),
	(r'(Neste)$', 'PREPOSICAO+PRONOME'),
	(r'(Nesta)$', 'PREPOSICAO+PRONOME'),
	(r'(Nestes)$', 'PREPOSICAO+PRONOME'),
	(r'(Nestas)$', 'PREPOSICAO+PRONOME'),
	(r'(Nisto)$', 'PREPOSICAO+PRONOME'),
	(r'(Nesse)$', 'PREPOSICAO+PRONOME'),
	(r'(Nessa)$', 'PREPOSICAO+PRONOME'),
	(r'(Nesses)$', 'PREPOSICAO+PRONOME'),
	(r'(Nessas)$', 'PREPOSICAO+PRONOME'),
	(r'(Nisso)$', 'PREPOSICAO+PRONOME'),
	(r'(Naquele)$', 'PREPOSICAO+PRONOME'),
	(r'(Naquela)$', 'PREPOSICAO+PRONOME'),
	(r'(Naqueles)$', 'PREPOSICAO+PRONOME'),
	(r'(Naquelas)$', 'PREPOSICAO+PRONOME'),
	(r'(Naquilo)$', 'PREPOSICAO+PRONOME'),
	(r'(Daqui)$', 'PREPOSICAO+ADVERBIO'),
	(r'(Daí)$', 'PREPOSICAO+ADVERBIO'),
	(r'(Dai)$', 'PREPOSICAO+ADVERBIO'),
	(r'(Dali)$', 'PREPOSICAO+ADVERBIO'),
	(r'(Dalém)$', 'PREPOSICAO+ADVERBIO'),
	(r'(Dalem)$', 'PREPOSICAO+ADVERBIO'),
	(r'(Aonde)$', 'PREPOSICAO+ADVERBIO'),
	(r'(Donde)$', 'PREPOSICAO+ADVERBIO'),

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
print(nltk.tag.accuracy(tag, test))
#verficar a precisao no NLTK 2.0
#tag.evaluate(test)




#SAVE TRAIN FILE
filename = 'wiki.tag.obj'
print("Salvando arquivo "+filename)
file_tag = open(filename, 'w') 
pickle.dump(tag, file_tag) 




print("Base finalizada")