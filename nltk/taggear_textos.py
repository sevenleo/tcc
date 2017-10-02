#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#import unidecode
#unaccented_string = unidecode.unidecode(txt)
import pickle
import nltk
from nltk.corpus import mac_morpho, stopwords


#__________________________________________________________________________

definitions = {
    'ART': 'artigo',
    'ADJ': 'adjetivo',
    'N': 'nome',
    'NPROP': 'nome proprio',
    'NUM': 'numeral',
    'PROADJ': 'pronome adjetivo',
    'PROSUB': 'pronome substantivo',
    'PROPESS': 'pronome pessoal',
    'PRO-KS': 'pronome conectivo subordinativo',
    'PRO-KS-REL': 'pronome conectivo subordinativo relativo',
    'ADV': 'adverbio',
    'ADV-KS': 'adverbio conectivo subordinativo',
    'ADV-KS-REL': 'adverbio relativo subordinativo',
    'KC': 'conjuncao cordenativa',
    'KS': 'conjuncao subordinativa',
    'PREP': 'preposicao',
    'IN': 'interjeicao',
    'V': 'verbo',
    'VAUX': 'verbo auxiliar',
    'PCP': 'participio',
    'PDEN': 'palavra denotativa',
    'CUR': 'simbolo de moeda corrente'

    #devo retirar isso daqui e adicionar como stopword
    #,',' :   'virgula',
    #'.' :   'ponto',
    #'!' :   'exclamacao',
    #'?' :   'interrogacao'
}

complement = {
    'EST': 'estrangeirismo',
    'AP': 'apostos',
    'DAD': 'dados',
    'TEL': 'telefone',
    'DAT': 'data',
    'HOR': 'hora',

}

connectors = {
    '|': 'complemento',
    '|+': 'contracoes e eclises',
    '|!': 'mesoclise',
}

#__________________________________________________________________________


lang = 'portuguese'
#train = mac_morpho.tagged_sents()[100:]
#test = mac_morpho.tagged_sents()[:100]


#__________________________________________________________________________


#LOAD TRAINED FILE
file_tag3_mac = open('tag3_mac.obj', 'r') 
tag3_mac = pickle.load(file_tag3_mac) 



#__________________________________________________________________________



#FUNCOES DE ANALISE
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
    return tag3_mac.tag(words)



def tag_word(word):
    return tag3_mac.tag([word])


#__________________________________________________________________________



#FRASE
pensamento_original="Pensamento e pensar são, respectivamente, uma forma de processo mental ou faculdade do sistema mental.[1] Pensar permite aos seres modelarem sua percepção do mundo ao redor de si, e com isso lidar com ele de uma forma efetiva e de acordo com suas metas, planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognição, senciência, consciência, ideia, e imaginação. O pensamento é considerado a expressão mais 'palpável' do espírito humano, pois através de imagens e ideias revela justamente a vontade deste. O pensamento é fundamental no processo de aprendizagem (vide Piaget). O pensamento é construto e construtivo do conhecimento. O principal veículo do processo de conscientização é o pensamento. A atividade de pensar confere ao homem 'asas' para mover-se no mundo e 'raízes' para aprofundar-se na realidade. Etimologicamente, pensar significa avaliar o peso de alguma coisa. Em sentido amplo, podemos dizer que o pensamento tem como missão tornar-se avaliador da realidade."
#  https://www.miniwebtool.com/remove-accent/
pensamento_sem_acentos="Pensamento e pensar sao, respectivamente, uma forma de processo mental ou faculdade do sistema mental.[1] Pensar permite aos seres modelarem sua percepcao do mundo ao redor de si, e com isso lidar com ele de uma forma efetiva e de acordo com suas metas, planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognicao, senciencia, consciencia, ideia, e imaginacao. O pensamento e considerado a expressao mais 'palpavel' do espirito humano, pois atraves de imagens e ideias revela justamente a vontade deste. O pensamento e fundamental no processo de aprendizagem (vide Piaget). O pensamento e construto e construtivo do conhecimento. O principal veiculo do processo de conscientizacao e o pensamento. A atividade de pensar confere ao homem 'asas' para mover-se no mundo e 'raizes' para aprofundar-se na realidade. Etimologicamente, pensar significa avaliar o peso de alguma coisa. Em sentido amplo, podemos dizer que o pensamento tem como missao tornar-se avaliador da realidade."
pensamento="Pensamento e pensar sao respectivamente uma forma de processo mental ou faculdade do sistema mental. Pensar permite aos seres modelarem sua percepcao do mundo ao redor de si e com isso lidar com ele de uma forma efetiva e de acordo com suas metas planos e desejos. Palavras que se referem a conceitos e processos similares incluem cognicao senciencia consciencia ideia e imaginacao. O pensamento e considerado a expressao mais palpavel do espirito humano pois atraves de imagens e ideias revela justamente a vontade deste. O pensamento e fundamental no processo de aprendizagem. O pensamento e construto e construtivo do conhecimento. O principal veiculo do processo de conscientizacao e o pensamento. A atividade de pensar confere ao homem asas para mover-se no mundo e raizes para aprofundar-se na realidade. Etimologicamente pensar significa avaliar o peso de alguma coisa. Em sentido amplo podemos dizer que o pensamento tem como missao tornar-se avaliador da realidade."


print("Exemplo:\n"+pensamento+"\n")
while (True):
    print("___________________________________________")
    entrada = raw_input("Digite o texto que deseja classificar:\n")
    if entrada=="":
        break
    tagged = tag_text(entrada)



    #CLASSIFICADAS
    print("\n\n* Palavra / Classificacao: *")
    for t in tagged:
        if t[1] != "unk":
            if t[1].split("|")[0] in definitions:
                classification = definitions[t[1].split("|")[0]]
            
            else:
                classification = "Simbolo ou pontuacao"
            
            print(t[0].upper()+"  ("+classification +")\n")




    #CLASSIFICACAO DESCONHECIDA
    print("\n\n** Palavras nao classificadas: **")
    for t in tagged:
        if t[1] == "unk":
            print(t[0])


    #print(stopwords.words(lang))
