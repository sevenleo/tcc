#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import time
start = time.time()


print ("==========================INICIANDO\n")

import json
import sys
import os
import nltk
import pickle
from nltk.corpus import mac_morpho, floresta, stopwords
lang = 'portuguese'



if len(sys.argv) >=2:
    DEBUG = False
else:
    DEBUG = True





print ("==========================DATASET(S)\n")
mac=False
floresta=False
wiki=False
test = False

if DEBUG:
    dataset="DEBUG"
else:
    dataset = raw_input(
        "Escolha o dataset:\n \
        * [MAC]_morpho\n \
        * [FLOR]esta\n \
        * Ambos [2]\n \
        * [WIKI]\t[default]\n \
        * TODOS [3]\n \
    ")

if dataset.lower() == "mac":
    mac=True
elif dataset.lower() == "wiki":
    wiki=True
elif dataset.lower() == "flor":
    floresta=True
elif dataset=="2":
    mac=True
    floresta=True
elif dataset=="3":
    mac=True
    floresta=True
    wiki=True
else:
    wiki=True




print ("==========================CARREGANDO ARQUIVOS tag\n")

#LOAD MAC_MORPHO TRAINED FILE
if mac==True:
    file='tag/tag_mac.obj'
    tag_mac = pickle.load(open(file, 'r'))
    print(file) 

#LOAD FLORESTA TRAINED FILE
if floresta==True:
    file='tag/tag_floresta.obj'
    tag_floresta = pickle.load(open(file, 'r')) 
    print(file) 

#LOAD TESTE FILE
if wiki==True:
    file='wiki.tag.obj'
    tag_wiki = pickle.load(open(file, 'r'))     
    print(file)

    #o json nao esta sendo salvo, logo carrega vazio
    #filejson=open('wiki_tag.json').read()
    #tag_wiki = json.loads(filejson)



print ("==========================CARREGANDO FUNCOES\n")

def relevant_words(text, RemoveStopwords = False):
    sentences = nltk.sent_tokenize(text, lang)
    words = []
    for sent in sentences:
        for word in nltk.word_tokenize(sent, lang):
            words.append(word)

    sws = stopwords.words(lang)
    if RemoveStopwords:
        relevant = []
        for word in words:
            if word not in sws:
                relevant.append(word)
    else:
        relevant = words
    return relevant



def tag_text(text, RemoveStopwords = False):
    words = relevant_words(text,RemoveStopwords)
    result = ["","",""]
    if mac==True:
        result[0] = tag_mac.tag(words)
    if floresta==True:
        result[1] = tag_floresta.tag(words)
    if wiki==True:
    	result[2] = tag_wiki.tag(words)
    return result
 


def tag_word(word):
    result = ["","",""]
    if mac==True:
        result[0] = tag_mac.tag([word])
    if floresta==True:
        result[1] = tag_floresta.tag([word])
    if wiki==True:
        result[2] = tag_wiki.tag([word])
    return result
 


if DEBUG==False:
    print ("==========================EXEMPLO\n")
    #FRASE
    pensamento="Pensamento e pensar sao respectivamente uma forma de processo mental ou faculdade do sistema mental. Pensar permite aos seres modelarem sua percepcao do mundo ao redor de si e com isso lidar com ele de uma forma efetiva e de acordo com suas metas planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognicao senciencia consciencia ideia e imaginacao. O pensamento e considerado a expressao mais palpavel do espirito humano pois atraves de imagens e ideias revela justamente a vontade deste. O pensamento e fundamental no processo de aprendizagem. O pensamento e construto e construtivo do conhecimento. O principal veiculo do processo de conscientizacao e o pensamento. A atividade de pensar confere ao homem asas para mover-se no mundo e raizes para aprofundar-se na realidade. Etimologicamente pensar significa avaliar o peso de alguma coisa. Em sentido amplo podemos dizer que o pensamento tem como missao tornar-se avaliador da realidade."
    print("Exemplo:\n"+pensamento+"\n")



while(True):
    print ("==========================ENTRADA DE TEXTO\n")
    if DEBUG:
        entrada = "Oi amigos, todos vocês irão viajar na viagem da semana que vem ?"
        print("Modo Debug:")
        print(entrada)
    else:
        entrada = raw_input("Digite o texto que deseja classificar:\n").lower()
        if entrada=="":
            break
        if entrada.startswith("---"):
            entrada=entrada.split("---")[1]
            os.system("clear")

    entrada = entrada.decode("utf-8")
    print(entrada)
    #TOKENIZAR
    tokens=[]
    for word in nltk.word_tokenize(entrada, lang):
            tokens.append(word)
    print("\n\nTokens  : "+str(len(tokens)))
            

    #TAGGED SENTS
    tags = tag_text(entrada)

    
    #tabela
    from terminaltables import AsciiTable
    table_data = []
 




    #CLASSIFICACOES
    table_data.append(["Palavra:","(mac_morpho)","(floresta)","(wiki_pessoal)"])
    for w in range(0,len(tokens)):
        linha = [tokens[w].upper()]
        if mac:
            linha.append(tags[0][w][1].lower())
        else:
            linha.append(" ")  
        if floresta:
            linha.append(tags[1][w][1].lower())
        else:
            linha.append(" ")  
        if wiki:
            linha.append(tags[2][w][1].lower())
        else:
            linha.append(" ")  

        #print(linha)
        table_data.append(linha)

    table = AsciiTable(table_data)
    print (table.table)

    if DEBUG:
        break
end = time.time()
print("\nTempo de execucao: "+str(end - start)+" seg")