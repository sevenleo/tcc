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



#NOVA(S) FRASE(S)

#Uma ideia é um veículo de motivação para a mudança e várias ideias formam raizes para a conscientização. (leonardo neves silva)

insert = [ 
    [ (u'Uma', u'ART'), (u'ideia', u'ADJ'), (u'é', u'V'), (u'um', u'ART'), (u'veículo', u'N '), (u'de', u'PREP'), (u'motivação', u'N '), (u'para', u'PREP'), (u'a', u'ART'), (u'mudança', u'N'), (u'e', u'KC'), (u'várias', u'PRO'), (u'ideias', u'N'), (u'formam', u'V'), (u'raizes', u'N'), (u'para', u'PREP'), (u'a', u'ART'), (u'conscientização', u'N'), (u'.', u'.'), (u'(', u'('), (u'leonardo', u'NPROP'), (u'neves', u'NPROP'), (u'silva', u'NPROP'), (u')', u')') ] 
]



regex = [
    (r"^[A-Z0-9._%+-]+\@[A-Z0-9.-]+\.[A-Z]{2,}$", "email"),
    (r"^[01]?[0-9]\:[012345]\d", "hora"),
    (r"^[2][0-4]\:[012345]\d", "hora"),
    (r"\$\d+", "dinheiro"),
    (r"\d+", "NUM"),
]



#TRAIN_STORE
file_tag3_mac = open('tag3_mac.obj', 'r') 
tag0 = pickle.load(file_tag3_mac) 
tag1 = nltk.UnigramTagger(insert, backoff=tag0)
tagr1 = nltk.RegexpTagger(regex,backoff=tag1)
tag2 = nltk.BigramTagger(insert, backoff=tagr1)
tag3 = nltk.TrigramTagger(insert, backoff=tag2)


#SAVE TRAIN-TEST FILE
file_tag3 = open('tag3_test.obj', 'w') 
pickle.dump(tag3, file_tag3) 