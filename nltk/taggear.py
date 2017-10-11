print ("==========================INICIANDO\n")

import json
import os
import nltk
import pickle
from nltk.corpus import mac_morpho, floresta, stopwords
lang = 'portuguese'




DEBUG = False





print ("==========================DATASET(S)\n")
mac=False
floresta=False
wiki=False
test = False
ambos=False
todos=False

if DEBUG:
    dataset="DEBUG"
else:
    dataset = raw_input(
        "Escolha o dataset:\n \
        * [MAC]_morpho\n \
        * [FLOR]esta\n \
        * Ambos [2]\n \
        * [WIKI]\n \
        * TODOS [3]\t[default]\n \
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
    ambos=True
elif dataset=="3":
    mac=True
    floresta=True
    wiki=True
    todos=True
else:
    mac=True
    floresta=True
    wiki=True
    todos=True



print ("==========================CARREGANDO ARQUIVOS TAG3\n")

#LOAD MAC_MORPHO TRAINED FILE
if mac==True:
    file='tag3/tag3_mac.obj'
    tag3_mac = pickle.load(open(file, 'r'))
    print(file) 

#LOAD FLORESTA TRAINED FILE
if floresta==True:
    file='tag3/tag3_floresta.obj'
    tag3_floresta = pickle.load(open(file, 'r')) 
    print(file) 

#LOAD TESTE FILE
if wiki==True:
    file='wiki.tag3.obj'
    tag3_wiki = pickle.load(open(file, 'r'))     
    print(file) 




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
        result[0] = tag3_mac.tag(words)
    if floresta==True:
        result[1] = tag3_floresta.tag(words)
    if wiki==True:
    	result[2] = tag3_wiki.tag(words)
    return result
 


def tag_word(word):
    result = ["","",""]
    if mac==True:
        result[0] = tag3_mac.tag([word])
    if floresta==True:
        result[1] = tag3_floresta.tag([word])
    if wiki==True:
        result[2] = tag3_wiki.tag([word])
    return result
 


if DEBUG==False:
    print ("==========================EXEMPLO\n")
    #FRASE
    pensamento="Pensamento e pensar sao respectivamente uma forma de processo mental ou faculdade do sistema mental. Pensar permite aos seres modelarem sua percepcao do mundo ao redor de si e com isso lidar com ele de uma forma efetiva e de acordo com suas metas planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognicao senciencia consciencia ideia e imaginacao. O pensamento e considerado a expressao mais palpavel do espirito humano pois atraves de imagens e ideias revela justamente a vontade deste. O pensamento e fundamental no processo de aprendizagem. O pensamento e construto e construtivo do conhecimento. O principal veiculo do processo de conscientizacao e o pensamento. A atividade de pensar confere ao homem asas para mover-se no mundo e raizes para aprofundar-se na realidade. Etimologicamente pensar significa avaliar o peso de alguma coisa. Em sentido amplo podemos dizer que o pensamento tem como missao tornar-se avaliador da realidade."
    print("Exemplo:\n"+pensamento+"\n")


while(True):
    print ("==========================ENTRADA DE TEXTO\n")
    if DEBUG:
        entrada = "oi amigos, estou de volta"
        print("Modo Debug:")
        print(entrada)
    else:
        entrada = raw_input("Digite o texto que deseja classificar:\n").lower()
        if entrada=="":
            break
        if entrada.startswith("---"):
            entrada=entrada.split("---")[1]
            os.system("clear")

    #TOKENIZAR
    tokens=[]
    for word in nltk.word_tokenize(entrada, lang):
            tokens.append(word)
    print("\n\nTokens  : "+str(len(tokens)))
            

    #TAGGED SENTS
    tags = tag_text(entrada)

    
    #CLASSIFICACOES
    print("\n\nPalavra:\t(mac_morpho)\t(floresta)\t(wiki_pessoal)")
    print    ("        \t------------\t----------\t--------------")
    for w in range(0,len(tokens)):
        linha = tokens[w].upper()
        #for tagged_sent in tags:
        #    linha+="\t\t("+tagged_sent[w][1].lower()+") "
        if mac:
            linha+="\t\t("+tags[0][w][1].lower()+")"
        else:
            linha+="\t\t( )"
        if floresta:
            linha+="\t\t("+tags[1][w][1].lower()+")"
        else:
            linha+="\t\t( )"   
        if wiki:
            linha+="\t\t("+tags[2][w][1].lower()+")"
        else:
            linha+="\t\t( )"

        print(linha)

    if DEBUG:
        break
'''
oi amigos, voltei
[('oi', 'unk'), ('amigos', u'N'), (',', u','), ('voltei', u'V')]
[('oi', 'unk'), ('amigos', u'H+n'), (',', u','), ('voltei', 'unk')]
[('oi', u'INT'), ('amigos', u'SUBSTANTIVO'), (',', u'VIRGULA'), ('voltei', u'VERBO')]
'''