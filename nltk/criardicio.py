#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
INSTALAR
python 2.7

pip install nltk
pip install unidecode

import nltk
nltk.download('mac_morpho')
nltk.download('floresta')
nltk.download('machado')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
'''

"""
TESTAR:

https://github.com/fmaruki/Nltk-Tagger-Portuguese

https://github.com/ibichara/ptbr_postag
	sudo python setup.py install
	
	import nltk
	from nltk.corpus import mac_morpho, stopwords
	lang = 'portuguese'
	train = mac_morpho.tagged_sents()[100:]
	test = mac_morpho.tagged_sents()[:100]
	t0 = None
	t1 = None
	t2 = None
	t3 = None
	t0 = nltk.DefaultTagger('unk')
	t1 = nltk.UnigramTagger(train, backoff=t0)
	t2 = nltk.BigramTagger(train, backoff=t1)
	t3 = nltk.TrigramTagger(train, backoff=t2)
"""


'''
PASSO 1
baixar um texto
dar uma classificacao
tokenizar
fazer stemming nos tokens
classificar gramaticalmente os tokens_stemmizados (usando o mac_morpho de preferencia ou usando a api de um dicionario gratis qualquer)
salvar em um dicionario usando python

 

PASSO 2
selecionar varios textos da web do mesmo assunto
e adicionar ao dicionario daquele assunto



PASSO N
pegar textos de blogs de acordo com as hashtags e adicionar aos dicionarios em que a hashtag se classificar

'''













'''
#import unidecode
#unaccented_string = unidecode.unidecode(txt)
import pickle
import nltk

pensamento_original="Pensamento e pensar são, respectivamente, uma forma de processo mental ou faculdade do sistema mental.[1] Pensar permite aos seres modelarem sua percepção do mundo ao redor de si, e com isso lidar com ele de uma forma efetiva e de acordo com suas metas, planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognição, senciência, consciência, ideia, e imaginação. O pensamento é considerado a expressão mais 'palpável' do espírito humano, pois através de imagens e ideias revela justamente a vontade deste. O pensamento é fundamental no processo de aprendizagem (vide Piaget). O pensamento é construto e construtivo do conhecimento. O principal veículo do processo de conscientização é o pensamento. A atividade de pensar confere ao homem 'asas' para mover-se no mundo e 'raízes' para aprofundar-se na realidade. Etimologicamente, pensar significa avaliar o peso de alguma coisa. Em sentido amplo, podemos dizer que o pensamento tem como missão tornar-se avaliador da realidade."


#  https://www.miniwebtool.com/remove-accent/
pensamento_sem_acentos="Pensamento e pensar sao, respectivamente, uma forma de processo mental ou faculdade do sistema mental.[1] Pensar permite aos seres modelarem sua percepcao do mundo ao redor de si, e com isso lidar com ele de uma forma efetiva e de acordo com suas metas, planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognicao, senciencia, consciencia, ideia, e imaginacao. O pensamento e considerado a expressao mais 'palpavel' do espirito humano, pois atraves de imagens e ideias revela justamente a vontade deste. O pensamento e fundamental no processo de aprendizagem (vide Piaget). O pensamento e construto e construtivo do conhecimento. O principal veiculo do processo de conscientizacao e o pensamento. A atividade de pensar confere ao homem 'asas' para mover-se no mundo e 'raizes' para aprofundar-se na realidade. Etimologicamente, pensar significa avaliar o peso de alguma coisa. Em sentido amplo, podemos dizer que o pensamento tem como missao tornar-se avaliador da realidade."

pensamento="Pensamento e pensar sao respectivamente uma forma de processo mental ou faculdade do sistema mental. Pensar permite aos seres modelarem sua percepcao do mundo ao redor de si e com isso lidar com ele de uma forma efetiva e de acordo com suas metas planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognicao senciencia consciencia ideia e imaginacao. O pensamento e considerado a expressao mais palpavel do espirito humano pois atraves de imagens e ideias revela justamente a vontade deste. O pensamento e fundamental no processo de aprendizagem. O pensamento e construto e construtivo do conhecimento. O principal veiculo do processo de conscientizacao e o pensamento. A atividade de pensar confere ao homem asas para mover-se no mundo e raizes para aprofundar-se na realidade. Etimologicamente pensar significa avaliar o peso de alguma coisa. Em sentido amplo podemos dizer que o pensamento tem como missao tornar-se avaliador da realidade."

frases = nltk.data.load("tokenizers/punkt/portuguese.pickle").tokenize(pensamento)

tokens_frases = [ nltk.word_tokenize(frase) for frase in frases]

for token in tokens_frases:
	print("\n"+str(token))

'''










import nltk
from nltk.corpus import mac_morpho, stopwords
lang = 'portuguese'
train = mac_morpho.tagged_sents()[:100]
test = mac_morpho.tagged_sents()[:100]
t0 = None
t1 = None
t2 = None
t3 = None
#t0 = nltk.DefaultTagger('unk')
#t1 = nltk.UnigramTagger(train, backoff=t0)
#t2 = nltk.BigramTagger(train, backoff=t1)
t3 = nltk.TrigramTagger(train, backoff=t2)

text="eu estou em uma casa amarela"

def split_into_relevant_words(self, text, bRemoveStopwords = False):
    sentences = nltk.sent_tokenize(text, slang)
    words = []
    for sent in sentences:
        for w in nltk.word_tokenize(sent, lang):
            words.append(w)

    sws = stopwords.words(lang)
    if bRemoveStopwords:
        relevant = []
        for w in words:
            if w not in sws:
                relevant.append(w)
    else:
        relevant = words
    return relevant

def tag_text(text, bRemoveStopwords):
    words = split_into_relevant_words(text)
    return t3.tag(words)

def tag_word(word):
    return t3.tag([word])

tag_text(text)